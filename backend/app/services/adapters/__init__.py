"""Abstract SourceAdapter interface — all news sources implement this."""

from __future__ import annotations

import hashlib
from abc import ABC, abstractmethod
from typing import List, Optional

from app.schemas.article import ArticleCreate


class SourceAdapter(ABC):
    """Base class for all news source adapters.

    Every adapter must:
    1. Implement `fetch_articles()` to return normalized ArticleCreate objects.
    2. Fall back to mock data when the API key is missing.
    3. Declare which category slugs it primarily covers.
    """

    name: str  # e.g. "newsapi", "guardian", "gnews"
    supported_categories: List[str] = []  # e.g. ["world", "technology", "business"]

    @abstractmethod
    async def fetch_articles(
        self,
        query: str = "latest news",
        category: Optional[str] = None,
    ) -> List[ArticleCreate]:
        """Fetch and normalize articles from this source.

        Args:
            query: Search query (default: general latest news).
            category: Optional category slug to filter by at the source level.
        """
        ...

    @staticmethod
    def compute_hash(title: str, url: str) -> str:
        """Deterministic content hash for deduplication."""
        raw = f"{title.strip().lower()}|{url.strip().lower()}"
        return hashlib.sha256(raw.encode()).hexdigest()
