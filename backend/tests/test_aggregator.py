"""Tests for the aggregator service — fetch + dedup logic."""

from __future__ import annotations

import pytest

from app.services.aggregator import fetch_all_sources


class TestAggregator:
    """Tests for the aggregator orchestration."""

    @pytest.mark.asyncio
    async def test_fetch_all_sources_returns_articles(self) -> None:
        """Without API keys, all adapters fall back to mock data."""
        articles = await fetch_all_sources()
        assert isinstance(articles, list)
        assert len(articles) > 0

    @pytest.mark.asyncio
    async def test_fetch_all_sources_deduplicates(self) -> None:
        """Content hashes should be unique across the result set."""
        articles = await fetch_all_sources()
        hashes = [a.content_hash for a in articles if a.content_hash]
        assert len(hashes) == len(set(hashes)), "Duplicate content hashes found"

    @pytest.mark.asyncio
    async def test_fetch_all_sources_articles_have_fields(self) -> None:
        articles = await fetch_all_sources()
        for a in articles:
            assert a.title
            assert a.url
            assert a.source
