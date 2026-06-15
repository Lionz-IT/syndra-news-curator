"""Bookmarks routes."""

from __future__ import annotations

import uuid
from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api.deps import CurrentUser, SessionDep
from app.models.article import Article
from app.models.bookmark import Bookmark
from app.schemas.article import ArticleRead
from app.schemas.bookmark import BookmarkRead

router = APIRouter(prefix="/bookmarks", tags=["bookmarks"])


@router.post("/{article_id}", response_model=BookmarkRead)
async def create_bookmark(
    session: SessionDep,
    current_user: CurrentUser,
    article_id: str,
) -> BookmarkRead:
    """Save an article to bookmarks."""
    try:
        uid = uuid.UUID(article_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid article ID format")

    # Check if article exists
    result = await session.execute(select(Article).where(Article.id == uid))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Article not found")

    # Check if already bookmarked
    stmt = select(Bookmark).where(
        Bookmark.user_id == current_user.id,
        Bookmark.article_id == uid
    )
    existing = await session.execute(stmt)
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Article already bookmarked")

    bookmark = Bookmark(user_id=current_user.id, article_id=uid)
    session.add(bookmark)
    await session.commit()
    await session.refresh(bookmark)
    
    return BookmarkRead.model_validate(bookmark)


@router.delete("/{article_id}")
async def delete_bookmark(
    session: SessionDep,
    current_user: CurrentUser,
    article_id: str,
) -> dict:
    """Remove an article from bookmarks."""
    try:
        uid = uuid.UUID(article_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid article ID format")

    stmt = select(Bookmark).where(
        Bookmark.user_id == current_user.id,
        Bookmark.article_id == uid
    )
    result = await session.execute(stmt)
    bookmark = result.scalar_one_or_none()

    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")

    await session.delete(bookmark)
    await session.commit()
    return {"status": "success"}


@router.get("", response_model=List[ArticleRead])
async def get_bookmarks(
    session: SessionDep,
    current_user: CurrentUser,
) -> List[ArticleRead]:
    """Get all bookmarked articles for the current user."""
    stmt = (
        select(Article)
        .join(Bookmark, Bookmark.article_id == Article.id)
        .where(Bookmark.user_id == current_user.id)
        .order_by(Bookmark.created_at.desc())
        .options(selectinload(Article.categories))
    )
    result = await session.execute(stmt)
    articles = result.scalars().all()
    
    return [ArticleRead.model_validate(a) for a in articles]
