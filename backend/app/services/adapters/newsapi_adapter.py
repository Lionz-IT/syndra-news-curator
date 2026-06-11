"""NewsAPI.org adapter — general news across all categories."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import List, Optional

import httpx

from app.core.config import get_settings
from app.schemas.article import ArticleCreate
from app.services.adapters import SourceAdapter
from app.services.adapters.mock_data import generate_mock_articles

logger = logging.getLogger(__name__)

# NewsAPI category → Syndra category slug mapping
_NEWSAPI_CATEGORY_MAP = {
    "general": "world",
    "business": "business",
    "technology": "technology",
    "science": "science",
    "health": "health",
    "sports": "sports",
    "entertainment": "entertainment",
}


class NewsAPIAdapter(SourceAdapter):
    """Adapter for NewsAPI.org (https://newsapi.org)."""

    name = "newsapi"
    supported_categories = list(_NEWSAPI_CATEGORY_MAP.values())

    def __init__(self) -> None:
        self.settings = get_settings()
        self.base_url = "https://newsapi.org/v2"

    async def fetch_articles(
        self,
        query: str = "latest news",
        category: Optional[str] = None,
    ) -> List[ArticleCreate]:
        if not self.settings.NEWSAPI_KEY:
            logger.info("NewsAPI key not set — returning mock data.")
            return generate_mock_articles(source_name=self.name, count=10)

        articles: List[ArticleCreate] = []

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                # Use top-headlines for category browsing, everything for search
                if category and category in _NEWSAPI_CATEGORY_MAP:
                    newsapi_cat = next(
                        (k for k, v in _NEWSAPI_CATEGORY_MAP.items() if v == category),
                        "general",
                    )
                    resp = await client.get(
                        f"{self.base_url}/top-headlines",
                        params={
                            "apiKey": self.settings.NEWSAPI_KEY,
                            "category": newsapi_cat,
                            "language": "en",
                            "pageSize": 20,
                        },
                    )
                else:
                    resp = await client.get(
                        f"{self.base_url}/everything",
                        params={
                            "apiKey": self.settings.NEWSAPI_KEY,
                            "q": query,
                            "language": "en",
                            "sortBy": "publishedAt",
                            "pageSize": 20,
                        },
                    )

                resp.raise_for_status()
                data = resp.json()

                for item in data.get("articles", []):
                    if not item.get("title") or item["title"] == "[Removed]":
                        continue

                    published_at = None
                    if item.get("publishedAt"):
                        try:
                            published_at = datetime.fromisoformat(
                                item["publishedAt"].replace("Z", "+00:00")
                            )
                        except (ValueError, TypeError):
                            pass

                    url = item.get("url", "")
                    title = item.get("title", "")
                    cat_slugs = [_NEWSAPI_CATEGORY_MAP.get(category, "world")] if category else ["world"]

                    articles.append(
                        ArticleCreate(
                            title=title,
                            body=item.get("content") or item.get("description"),
                            summary=item.get("description"),
                            url=url,
                            image_url=item.get("urlToImage"),
                            source=self.name,
                            author=item.get("author"),
                            language="en",
                            category_slugs=cat_slugs,
                            raw_tags=[],
                            published_at=published_at,
                            content_hash=self.compute_hash(title, url),
                        )
                    )

        except httpx.HTTPError as e:
            logger.warning("NewsAPI request failed: %s — falling back to mock data.", e)
            return generate_mock_articles(source_name=self.name, count=10)

        return articles or generate_mock_articles(source_name=self.name, count=5)
