"""RSS feed adapter — aggregates from multiple RSS/Atom feeds."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Dict, List, Optional

import feedparser
import httpx

from app.schemas.article import ArticleCreate
from app.services.adapters import SourceAdapter
from app.services.adapters.mock_data import generate_mock_articles

logger = logging.getLogger(__name__)

# ── Feed registry: URL → metadata ────────────────────────
# Each feed has a name, URL, and category slugs it primarily covers.
# No API keys needed — RSS is open.

RSS_FEEDS: List[Dict] = [
    # Energy & Sustainability
    {
        "name": "IEA News",
        "url": "https://www.iea.org/news/rss",
        "category_slugs": ["energy", "energy-policy"],
        "region": "global",
    },
    {
        "name": "IRENA News",
        "url": "https://www.irena.org/News/rss",
        "category_slugs": ["energy", "energy-solar", "energy-wind"],
        "region": "global",
    },
    {
        "name": "CleanTechnica",
        "url": "https://cleantechnica.com/feed/",
        "category_slugs": ["energy", "energy-ev", "energy-solar"],
        "region": "global",
    },
    {
        "name": "Renewable Energy World",
        "url": "https://www.renewableenergyworld.com/feed/",
        "category_slugs": ["energy", "energy-wind", "energy-solar"],
        "region": "north-america",
    },
    # General / World
    {
        "name": "BBC World",
        "url": "http://feeds.bbci.co.uk/news/world/rss.xml",
        "category_slugs": ["world"],
        "region": "global",
    },
    {
        "name": "Reuters World",
        "url": "https://www.reutersagency.com/feed/",
        "category_slugs": ["world", "business"],
        "region": "global",
    },
    {
        "name": "Al Jazeera",
        "url": "https://www.aljazeera.com/xml/rss/all.xml",
        "category_slugs": ["world", "politics"],
        "region": "middle-east",
    },
    # Technology
    {
        "name": "Ars Technica",
        "url": "https://feeds.arstechnica.com/arstechnica/index",
        "category_slugs": ["technology", "science"],
        "region": "north-america",
    },
    {
        "name": "TechCrunch",
        "url": "https://techcrunch.com/feed/",
        "category_slugs": ["technology", "business-startups"],
        "region": "north-america",
    },
    # Science
    {
        "name": "Nature News",
        "url": "https://www.nature.com/nature.rss",
        "category_slugs": ["science"],
        "region": "global",
    },
    # Sports
    {
        "name": "ESPN",
        "url": "https://www.espn.com/espn/rss/news",
        "category_slugs": ["sports"],
        "region": "north-america",
    },
    # UN SDG News
    {
        "name": "UN SDG News",
        "url": "https://news.un.org/feed/subscribe/en/news/topic/sdgs/feed/rss.xml",
        "category_slugs": ["world", "environment", "energy"],
        "region": "global",
    },
]


class RSSAdapter(SourceAdapter):
    """Adapter that aggregates articles from multiple RSS/Atom feeds."""

    name = "rss"
    supported_categories = [
        "energy", "energy-policy", "energy-solar", "energy-wind", "energy-ev",
        "world", "business", "technology", "science", "sports",
        "politics", "environment",
    ]

    async def fetch_articles(
        self,
        query: str = "latest news",
        category: Optional[str] = None,
    ) -> List[ArticleCreate]:
        articles: List[ArticleCreate] = []

        # Filter feeds by category if specified
        feeds = RSS_FEEDS
        if category:
            feeds = [f for f in RSS_FEEDS if category in f.get("category_slugs", [])]
            if not feeds:
                feeds = RSS_FEEDS[:3]  # fallback to first few

        for feed_meta in feeds:
            try:
                feed_articles = await self._fetch_single_feed(feed_meta)
                articles.extend(feed_articles)
            except Exception as e:
                logger.warning("Failed to fetch RSS feed %s: %s", feed_meta["name"], e)
                continue

        if not articles:
            logger.info("No RSS articles fetched — returning mock data.")
            return generate_mock_articles(source_name=self.name, count=8)

        return articles

    async def _fetch_single_feed(self, feed_meta: Dict) -> List[ArticleCreate]:
        """Fetch and parse a single RSS feed."""
        articles: List[ArticleCreate] = []

        try:
            async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
                resp = await client.get(feed_meta["url"])
                resp.raise_for_status()
                content = resp.text
        except httpx.HTTPError as e:
            logger.debug("HTTP error fetching %s: %s", feed_meta["url"], e)
            return []

        feed = feedparser.parse(content)

        for entry in feed.entries[:15]:  # cap per feed
            title = entry.get("title", "").strip()
            link = entry.get("link", "").strip()

            if not title or not link:
                continue

            # Parse publish date
            published_at = None
            for date_field in ("published_parsed", "updated_parsed"):
                parsed = entry.get(date_field)
                if parsed:
                    try:
                        published_at = datetime(*parsed[:6], tzinfo=timezone.utc)
                    except (TypeError, ValueError):
                        pass
                    break

            if not published_at and entry.get("published"):
                try:
                    published_at = parsedate_to_datetime(entry["published"])
                except (TypeError, ValueError):
                    pass

            # Extract body/summary
            body = ""
            if entry.get("content"):
                body = entry.content[0].get("value", "")
            summary = entry.get("summary", entry.get("description", ""))

            # Image
            image_url = None
            for link_item in entry.get("links", []):
                if link_item.get("type", "").startswith("image"):
                    image_url = link_item.get("href")
                    break
            if not image_url and entry.get("media_content"):
                image_url = entry.media_content[0].get("url")

            articles.append(
                ArticleCreate(
                    title=title,
                    body=body or None,
                    summary=summary[:500] if summary else None,
                    url=link,
                    image_url=image_url,
                    source=f"rss-{feed_meta['name'].lower().replace(' ', '-')}",
                    author=entry.get("author"),
                    language="en",
                    region=feed_meta.get("region"),
                    category_slugs=feed_meta.get("category_slugs", []),
                    raw_tags=[t.get("term", "") for t in entry.get("tags", [])],
                    published_at=published_at,
                    content_hash=self.compute_hash(title, link),
                )
            )

        return articles
