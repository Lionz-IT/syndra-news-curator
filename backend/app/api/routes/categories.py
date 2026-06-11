"""Categories API — returns the hierarchical category taxonomy."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryListResponse, CategoryTree

router = APIRouter(prefix="/categories", tags=["categories"])


def _model_to_tree(cat: Category) -> CategoryTree:
    """Recursively convert a Category ORM model to a CategoryTree schema."""
    return CategoryTree(
        id=cat.id,
        name=cat.name,
        slug=cat.slug,
        description=cat.description,
        icon=cat.icon,
        color=cat.color,
        display_order=cat.display_order,
        parent_id=cat.parent_id,
        created_at=cat.created_at,
        children=[_model_to_tree(child) for child in (cat.children or [])],
    )


@router.get("", response_model=CategoryListResponse)
async def list_categories(db: AsyncSession = Depends(get_db)) -> CategoryListResponse:
    """Return the full category tree (top-level categories with nested children)."""
    stmt = (
        select(Category)
        .where(Category.parent_id.is_(None))
        .options(selectinload(Category.children).selectinload(Category.children))
        .order_by(Category.display_order, Category.name)
    )
    result = await db.execute(stmt)
    roots = result.scalars().unique().all()

    tree = [_model_to_tree(cat) for cat in roots]
    return CategoryListResponse(items=tree, total=len(tree))


@router.get("/{slug}", response_model=CategoryTree)
async def get_category_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_db),
) -> CategoryTree:
    """Return a single category by slug, with its children."""
    stmt = (
        select(Category)
        .where(Category.slug == slug)
        .options(selectinload(Category.children))
    )
    result = await db.execute(stmt)
    cat = result.scalar_one_or_none()
    if cat is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"Category '{slug}' not found")
    return _model_to_tree(cat)
