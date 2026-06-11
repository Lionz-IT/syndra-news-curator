"""Pydantic schemas for Category — API request/response models."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    name: str = Field(..., max_length=128)
    slug: str = Field(..., max_length=128)
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    display_order: int = 0


class CategoryRead(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    parent_id: Optional[UUID] = None
    created_at: datetime


class CategoryTree(CategoryRead):
    """Category with nested children for tree responses."""
    children: List[CategoryTree] = []


class CategoryListResponse(BaseModel):
    items: List[CategoryTree]
    total: int
