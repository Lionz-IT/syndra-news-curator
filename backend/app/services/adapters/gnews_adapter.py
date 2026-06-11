"""GNews API adapter — global multilingual news."""

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

# GNews topic → Syndra category slug mapping
_GNEWS_TOPIC_MAP = {
    "world": "world",
    "nation": "politics",
    "business": "business",
    "technology": "technology",
    "science": "science",
    "health": "health",
    "sports": "sports",
    "entertainment": "entertainment",
}


class GNewsAdapter(SourceAdapter):
    """Adapter for GNews API (https://gnews.io)."""

    name = "gnews"
    supported_categories = list(_GNEWS_TOPIC_MAP.values())

    def __init__(self) -> None:
        self.settings = get_settings()
        self.base_url = "https://gnews.io/api/v4"

    async def fetch_articles(
        self,
        query: str = "latest news",
        category: Optional[str] = None,
    ) -> List[ArticleCreate]:
        if not self.settings.GNEWS_API_KEY:
            logger.info("GNews API key not set — returning mock data.")
            return generate_mock_articles(source_name=self.name, count=8)

        articles: List[ArticleCreate] = []

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                if category and category in _GNEWS_TOPIC_MAP:
                    gnews_topic = next(
                        (k for k, v in _GNEWS_TOPIC_MAP.items() if v == category),
                        "world",
                    )
                    resp = await client.get(
                        f"{self.base_url}/top-headlines",
                        params={
                            "token": self.settings.GNEWS_API_KEY,
                            "topic": gnews_topic,
                            "lang": "en",
                            "max": 20,
                        },
                    )
                else:
                    resp = await client.get(
                        f"{self.base_url}/search",
                        params={
                            "token": self.settings.GNEWS_API_KEY,
                            "q": query,
                            "lang": "en",
                            "max": 20,
                        },
                    )

                resp.raise_for_status()
                data = resp.json()

                for item in data.get("articles", []):
                    title = item.get("title", "")
                    url = item.get("url", "")

                    if not title or not url:
                        continue

                    published_at = None
                    if item.get("publishedAt"):
                        try:
                            published_at = datetime.fromisoformat(
                                item["publishedAt"].replace("Z", "+00:00")
                            )
                        except (ValueError, TypeError):
                            pass

                    cat_slugs = [_GNEWS_TOPIC_MAP.get(category, "world")] if category else ["world"]

                    articles.append(
                        ArticleCreate(
                            title=title,
                            body=item.get("content"),
                            summary=item.get("description"),
                            url=url,
                            image_url=item.get("image"),
                            source=self.name,
                            author=item.get("source", {}).get("name"),
                            language="en",
                            category_slugs=cat_slugs,
                            raw_tags=[],
                            published_at=published_at,
                            content_hash=self.compute_hash(title, url),
                        )
                    )

        except httpx.HTTPError as e:
            logger.warning("GNews API request failed: %s — falling back to mock data.", e)
            return generate_mock_articles(source_name=self.name, count=8)

        return articles or generate_mock_articles(source_name=self.name, count=5)
