"""Tests for the /api/news endpoint route registration.

These tests verify that API routes are properly registered on the FastAPI app
without making HTTP calls that require a live PostgreSQL connection.
"""

from __future__ import annotations

from app.main import app


class TestNewsEndpoint:
    """Verify news/category routes are registered (no DB required)."""

    def test_news_endpoint_registered(self) -> None:
        """The /api/news route should be registered on the app."""
        paths = [route.path for route in app.routes]
        assert any("/api/news" in p for p in paths)

    def test_categories_endpoint_registered(self) -> None:
        """The /api/categories route should be registered on the app."""
        paths = [route.path for route in app.routes]
        assert any("/api/categories" in p for p in paths)

    def test_news_detail_endpoint_registered(self) -> None:
        """The /api/news/{article_id} route should be registered."""
        paths = [route.path for route in app.routes]
        assert any("/api/news/" in p for p in paths)
