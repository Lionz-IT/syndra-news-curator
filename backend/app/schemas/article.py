"""Pydantic schemas for Article — API request/response models."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.category import CategoryRead


# ── Shared base ───────────────────────────────────────────
class ArticleBase(BaseModel):
    title: str = Field(..., max_length=512)
    url: str = Field(..., max_length=2048)
    source: str = Field(..., max_length=128)
    language: str = Field(default="en", max_length=10)


# ── Creation (internal — from adapters) ───────────────────
class ArticleCreate(ArticleBase):
    body: Optional[str] = None
    summary: Optional[str] = None
    image_url: Optional[str] = None
    author: Optional[str] = None
    region: Optional[str] = None
    raw_tags: Optional[List[str]] = None
    published_at: Optional[datetime] = None
    content_hash: Optional[str] = None
    category_slugs: Optional[List[str]] = None  # resolved to Category M2M on insert


# ── API response ──────────────────────────────────────────
class ArticleRead(ArticleBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    body: Optional[str] = None
    summary: Optional[str] = None
    image_url: Optional[str] = None
    author: Optional[str] = None
    region: Optional[str] = None
    raw_tags: Optional[List[str]] = None
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    # Categories (M2M)
    categories: List[CategoryRead] = []

    # AI fields
    bias_score: Optional[float] = None
    bias_label: Optional[str] = None
    sdg_tags: Optional[List[str]] = None
    ai_summary: Optional[str] = None


# ── Paginated response ───────────────────────────────────
class ArticleListResponse(BaseModel):
    items: List[ArticleRead]
    total: int
    page: int
    page_size: int
    total_pages: int


# ── Query params ─────────────────────────────────────────
class ArticleFilters(BaseModel):
    source: Optional[str] = None
    category: Optional[str] = None             # single category slug
    categories: Optional[List[str]] = None     # multi-category slugs
    language: Optional[str] = None
    region: Optional[str] = None
    search: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    bias_score_min: Optional[float] = Field(default=None, ge=0, le=100)
    bias_score_max: Optional[float] = Field(default=None, ge=0, le=100)
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
