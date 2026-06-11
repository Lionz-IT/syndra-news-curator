"""Aggregator service — orchestrates fetching from all adapters, deduplicates, persists."""

from __future__ import annotations

import asyncio
import logging
from typing import Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.article import Article
from app.models.category import Category
from app.schemas.article import ArticleCreate
from app.services.adapters import SourceAdapter
from app.services.adapters.newsapi_adapter import NewsAPIAdapter
from app.services.adapters.guardian_adapter import GuardianAdapter
from app.services.adapters.gnews_adapter import GNewsAdapter
from app.services.adapters.rss_adapter import RSSAdapter

logger = logging.getLogger(__name__)


def get_all_adapters() -> List[SourceAdapter]:
    """Return instances of every registered source adapter."""
    return [
        NewsAPIAdapter(),
        GuardianAdapter(),
        GNewsAdapter(),
        RSSAdapter(),
    ]


async def fetch_all_sources(
    query: str = "latest news",
    category: Optional[str] = None,
) -> List[ArticleCreate]:
    """Fetch articles from ALL adapters concurrently, deduplicate by content_hash."""
    adapters = get_all_adapters()

    tasks = [adapter.fetch_articles(query=query, category=category) for adapter in adapters]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    all_articles: List[ArticleCreate] = []
    seen_hashes: set[str] = set()

    for i, result in enumerate(results):
        if isinstance(result, Exception):
            logger.warning(
                "Adapter %s failed: %s", adapters[i].name, result
            )
            continue

        for article in result:
            h = article.content_hash
            if h and h in seen_hashes:
                continue
            if h:
                seen_hashes.add(h)
            all_articles.append(article)

    logger.info(
        "Aggregated %d articles from %d adapters (%d dupes removed).",
        len(all_articles),
        len(adapters),
        sum(len(r) for r in results if isinstance(r, list)) - len(all_articles),
    )
    return all_articles


async def _resolve_categories(
    session: AsyncSession,
    slugs: List[str],
    cache: Dict[str, Category],
) -> List[Category]:
    """Resolve category slugs to Category ORM objects (cached per batch)."""
    categories: List[Category] = []
    for slug in slugs:
        if slug in cache:
            categories.append(cache[slug])
            continue
        result = await session.execute(
            select(Category).where(Category.slug == slug)
        )
        cat = result.scalar_one_or_none()
        if cat:
            cache[slug] = cat
            categories.append(cat)
    return categories


async def persist_articles(
    session: AsyncSession,
    articles: List[ArticleCreate],
) -> int:
    """Insert new articles into the DB, skip duplicates by content_hash.

    Returns the count of newly inserted articles.
    """
    if not articles:
        return 0

    # Collect all content hashes to check existing
    hashes = [a.content_hash for a in articles if a.content_hash]
    existing_hashes: set[str] = set()

    if hashes:
        result = await session.execute(
            select(Article.content_hash).where(Article.content_hash.in_(hashes))
        )
        existing_hashes = {row[0] for row in result.all() if row[0]}

    category_cache: Dict[str, Category] = {}
    inserted = 0

    for article_data in articles:
        if article_data.content_hash and article_data.content_hash in existing_hashes:
            continue

        # Build ORM object
        article = Article(
            title=article_data.title,
            body=article_data.body,
            summary=article_data.summary,
            url=article_data.url,
            image_url=article_data.image_url,
            source=article_data.source,
            author=article_data.author,
            language=article_data.language,
            region=article_data.region,
            raw_tags=article_data.raw_tags,
            published_at=article_data.published_at,
            content_hash=article_data.content_hash,
        )

        # Resolve M2M categories
        if article_data.category_slugs:
            cats = await _resolve_categories(
                session, article_data.category_slugs, category_cache
            )
            article.categories = cats

        session.add(article)
        inserted += 1

        if article_data.content_hash:
            existing_hashes.add(article_data.content_hash)

    if inserted:
        await session.flush()

    logger.info("Persisted %d new articles (%d skipped as dupes).", inserted, len(articles) - inserted)
    return inserted
