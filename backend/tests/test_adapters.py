"""Tests for source adapters — verify mock fallback works for all adapters."""

from __future__ import annotations

import pytest

from app.services.adapters.mock_data import generate_mock_articles
from app.services.adapters.newsapi_adapter import NewsAPIAdapter
from app.services.adapters.guardian_adapter import GuardianAdapter
from app.services.adapters.gnews_adapter import GNewsAdapter
from app.services.adapters.rss_adapter import RSSAdapter


class TestMockDataFactory:
    """Tests for the mock/seed data factory."""

    def test_generate_mock_articles_returns_list(self) -> None:
        articles = generate_mock_articles()
        assert isinstance(articles, list)
        assert len(articles) > 0

    def test_generate_mock_articles_with_count(self) -> None:
        articles = generate_mock_articles(count=5)
        assert len(articles) <= 5

    def test_generate_mock_articles_with_source_name(self) -> None:
        articles = generate_mock_articles(source_name="newsapi")
        assert all(a.source == "newsapi" for a in articles)

    def test_mock_articles_have_required_fields(self) -> None:
        articles = generate_mock_articles()
        for a in articles:
            assert a.title
            assert a.url
            assert a.source
            assert a.content_hash
            assert a.language

    def test_mock_articles_have_category_slugs(self) -> None:
        articles = generate_mock_articles()
        for a in articles:
            assert a.category_slugs is not None
            assert len(a.category_slugs) > 0

    def test_mock_articles_cover_multiple_categories(self) -> None:
        articles = generate_mock_articles()
        all_slugs = set()
        for a in articles:
            if a.category_slugs:
                all_slugs.update(a.category_slugs)
        # Should cover at least 5 different categories
        assert len(all_slugs) >= 5


class TestNewsAPIAdapter:
    """Tests for NewsAPI adapter (mock fallback, no real API key)."""

    @pytest.mark.asyncio
    async def test_fetch_returns_articles_without_api_key(self) -> None:
        adapter = NewsAPIAdapter()
        articles = await adapter.fetch_articles()
        assert isinstance(articles, list)
        assert len(articles) > 0

    def test_adapter_has_name(self) -> None:
        adapter = NewsAPIAdapter()
        assert adapter.name == "newsapi"

    def test_adapter_has_supported_categories(self) -> None:
        adapter = NewsAPIAdapter()
        assert len(adapter.supported_categories) > 0


class TestGuardianAdapter:
    """Tests for Guardian adapter (mock fallback)."""

    @pytest.mark.asyncio
    async def test_fetch_returns_articles_without_api_key(self) -> None:
        adapter = GuardianAdapter()
        articles = await adapter.fetch_articles()
        assert isinstance(articles, list)
        assert len(articles) > 0

    def test_adapter_has_name(self) -> None:
        adapter = GuardianAdapter()
        assert adapter.name == "guardian"


class TestGNewsAdapter:
    """Tests for GNews adapter (mock fallback)."""

    @pytest.mark.asyncio
    async def test_fetch_returns_articles_without_api_key(self) -> None:
        adapter = GNewsAdapter()
        articles = await adapter.fetch_articles()
        assert isinstance(articles, list)
        assert len(articles) > 0

    def test_adapter_has_name(self) -> None:
        adapter = GNewsAdapter()
        assert adapter.name == "gnews"


class TestRSSAdapter:
    """Tests for RSS adapter (mock fallback when feeds unreachable)."""

    @pytest.mark.asyncio
    async def test_fetch_returns_articles(self) -> None:
        adapter = RSSAdapter()
        # RSS feeds may fail in CI, but mock fallback should kick in
        articles = await adapter.fetch_articles()
        assert isinstance(articles, list)
        assert len(articles) > 0

    def test_adapter_has_name(self) -> None:
        adapter = RSSAdapter()
        assert adapter.name == "rss"
