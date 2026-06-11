"""The Guardian API adapter — quality journalism across sections."""

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

# Guardian section → Syndra category slug mapping
_GUARDIAN_SECTION_MAP = {
    "world": "world",
    "politics": "politics",
    "business": "business",
    "technology": "technology",
    "science": "science",
    "environment": "environment",
    "sport": "sports",
    "football": "sports-football",
    "culture": "arts-culture",
    "film": "entertainment-movies",
    "music": "entertainment-music",
    "lifeandstyle": "lifestyle",
    "education": "education",
    "law": "law",
    "travel": "lifestyle-travel",
    "food": "lifestyle-food",
    "opinion": "opinion",
}


class GuardianAdapter(SourceAdapter):
    """Adapter for The Guardian Open Platform (https://open-platform.theguardian.com)."""

    name = "guardian"
    supported_categories = list(set(_GUARDIAN_SECTION_MAP.values()))

    def __init__(self) -> None:
        self.settings = get_settings()
        self.base_url = "https://content.guardianapis.com"

    async def fetch_articles(
        self,
        query: str = "latest news",
        category: Optional[str] = None,
    ) -> List[ArticleCreate]:
        if not self.settings.GUARDIAN_API_KEY:
            logger.info("Guardian API key not set — returning mock data.")
            return generate_mock_articles(source_name=self.name, count=8)

        articles: List[ArticleCreate] = []

        try:
            params: dict = {
                "api-key": self.settings.GUARDIAN_API_KEY,
                "show-fields": "headline,trailText,body,thumbnail,byline",
                "page-size": 20,
                "order-by": "newest",
            }

            if category:
                # Find Guardian section for this category
                guardian_section = next(
                    (k for k, v in _GUARDIAN_SECTION_MAP.items() if v == category),
                    None,
                )
                if guardian_section:
                    params["section"] = guardian_section
                else:
                    params["q"] = query
            else:
                params["q"] = query

            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.get(f"{self.base_url}/search", params=params)
                resp.raise_for_status()
                data = resp.json()

                for item in data.get("response", {}).get("results", []):
                    fields = item.get("fields", {})
                    title = fields.get("headline") or item.get("webTitle", "")
                    url = item.get("webUrl", "")

                    if not title or not url:
                        continue

                    published_at = None
                    if item.get("webPublicationDate"):
                        try:
                            published_at = datetime.fromisoformat(
                                item["webPublicationDate"].replace("Z", "+00:00")
                            )
                        except (ValueError, TypeError):
                            pass

                    section = item.get("sectionId", "")
                    cat_slug = _GUARDIAN_SECTION_MAP.get(section, "world")

                    articles.append(
                        ArticleCreate(
                            title=title,
                            body=fields.get("body"),
                            summary=fields.get("trailText"),
                            url=url,
                            image_url=fields.get("thumbnail"),
                            source=self.name,
                            author=fields.get("byline"),
                            language="en",
                            category_slugs=[cat_slug],
                            raw_tags=[item.get("sectionName", "")] if item.get("sectionName") else [],
                            published_at=published_at,
                            content_hash=self.compute_hash(title, url),
                        )
                    )

        except httpx.HTTPError as e:
            logger.warning("Guardian API request failed: %s — falling back to mock data.", e)
            return generate_mock_articles(source_name=self.name, count=8)

        return articles or generate_mock_articles(source_name=self.name, count=5)
