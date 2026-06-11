"""Category model — hierarchical taxonomy for news classification."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.article import Article

# ── M2M join table: articles <-> categories ───────────────
article_categories = Table(
    "article_categories",
    Base.metadata,
    Column("article_id", UUID(as_uuid=True), ForeignKey("articles.id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", UUID(as_uuid=True), ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True),
)


class Category(Base):
    """Hierarchical news category (data-driven, not hardcoded)."""

    __tablename__ = "categories"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    slug: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    icon: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    color: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # ── Hierarchy ─────────────────────────────────────────
    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, index=True
    )
    parent: Mapped[Optional[Category]] = relationship(
        "Category", remote_side="Category.id", back_populates="children", lazy="selectin"
    )
    children: Mapped[List[Category]] = relationship(
        "Category", back_populates="parent", lazy="selectin", order_by="Category.display_order"
    )

    # ── M2M to articles ───────────────────────────────────
    articles: Mapped[List[Article]] = relationship(
        "Article", secondary=article_categories, back_populates="categories", lazy="noload"
    )

    # ── Timestamps ────────────────────────────────────────
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        return f"<Category {self.slug}>"
