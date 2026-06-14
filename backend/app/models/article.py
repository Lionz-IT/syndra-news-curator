"""Article model — core entity for aggregated news."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import DateTime, Float, Index, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.category import Category

from app.models.category import article_categories


class Article(Base):
    """Normalized article from any news source."""

    __tablename__ = "articles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # ── Content ───────────────────────────────────────────
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    body: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    url: Mapped[str] = mapped_column(String(2048), nullable=False, unique=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(2048), nullable=True)

    # ── Metadata ──────────────────────────────────────────
    source: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    author: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    language: Mapped[str] = mapped_column(String(10), nullable=False, default="en")
    region: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    raw_tags: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True)

    # ── Categories (M2M — replaces old flat `category` column) ─
    categories: Mapped[List[Category]] = relationship(
        "Category", secondary=article_categories, back_populates="articles", lazy="selectin"
    )

    # ── Timestamps ────────────────────────────────────────
    published_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )
    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # ── AI / NLP (populated later in pipeline) ────────────
    bias_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    bias_label: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    sdg_tags: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True)
    ai_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # ── Dedup ─────────────────────────────────────────────
    content_hash: Mapped[Optional[str]] = mapped_column(
        String(64), nullable=True, unique=True, index=True
    )

    __table_args__ = (
        Index("ix_articles_source_published", "source", "published_at"),
        Index("ix_articles_language", "language"),
    )

    def __repr__(self) -> str:
        return f"<Article {self.source}: {self.title[:50]}>"
