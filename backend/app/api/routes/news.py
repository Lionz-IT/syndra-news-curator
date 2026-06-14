"""News API endpoint — list, filter, search articles."""

from __future__ import annotations

import math
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.article import Article
from app.models.category import Category, article_categories
from app.schemas.article import ArticleListResponse, ArticleRead

router = APIRouter(prefix="/news", tags=["news"])


@router.get("", response_model=ArticleListResponse)
async def list_articles(
    # ── Filters ────────────────────────────────────────
    source: Optional[str] = Query(None, description="Filter by source name"),
    category: Optional[str] = Query(None, description="Filter by single category slug"),
    categories: Optional[str] = Query(None, description="Comma-separated category slugs"),
    language: Optional[str] = Query(None, description="Filter by language code"),
    region: Optional[str] = Query(None, description="Filter by region"),
    search: Optional[str] = Query(None, description="Full-text search in title/body"),
    date_from: Optional[datetime] = Query(None, description="Articles published after this date"),
    date_to: Optional[datetime] = Query(None, description="Articles published before this date"),
    bias_score_min: Optional[float] = Query(None, ge=0, le=100, description="Minimum bias score"),
    bias_score_max: Optional[float] = Query(None, ge=0, le=100, description="Maximum bias score"),
    # ── Pagination ────────────────────────────────────
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    # ── DB ────────────────────────────────────────────
    db: AsyncSession = Depends(get_db),
) -> ArticleListResponse:
    """List articles with filtering, search, and pagination."""

    # ── Base query ────────────────────────────────────
    stmt = select(Article).options(selectinload(Article.categories))
    count_stmt = select(func.count(Article.id))

    # ── Apply filters ─────────────────────────────────
    if source:
        stmt = stmt.where(Article.source == source)
        count_stmt = count_stmt.where(Article.source == source)

    if language:
        stmt = stmt.where(Article.language == language)
        count_stmt = count_stmt.where(Article.language == language)

    if region:
        stmt = stmt.where(Article.region == region)
        count_stmt = count_stmt.where(Article.region == region)

    if date_from:
        stmt = stmt.where(Article.published_at >= date_from)
        count_stmt = count_stmt.where(Article.published_at >= date_from)

    if date_to:
        stmt = stmt.where(Article.published_at <= date_to)
        count_stmt = count_stmt.where(Article.published_at <= date_to)

    if bias_score_min is not None:
        stmt = stmt.where(Article.bias_score >= bias_score_min)
        count_stmt = count_stmt.where(Article.bias_score >= bias_score_min)

    if bias_score_max is not None:
        stmt = stmt.where(Article.bias_score <= bias_score_max)
        count_stmt = count_stmt.where(Article.bias_score <= bias_score_max)

    # ── Category filter (M2M join) ────────────────────
    cat_slugs: List[str] = []
    if category:
        cat_slugs = [category]
    elif categories:
        cat_slugs = [s.strip() for s in categories.split(",") if s.strip()]

    if cat_slugs:
        stmt = (
            stmt.join(article_categories, Article.id == article_categories.c.article_id)
            .join(Category, Category.id == article_categories.c.category_id)
            .where(Category.slug.in_(cat_slugs))
        )
        count_stmt = (
            count_stmt.join(article_categories, Article.id == article_categories.c.article_id)
            .join(Category, Category.id == article_categories.c.category_id)
            .where(Category.slug.in_(cat_slugs))
        )

    # ── Search (ILIKE on title + body) ────────────────
    if search:
        pattern = f"%{search}%"
        stmt = stmt.where(
            Article.title.ilike(pattern) | Article.body.ilike(pattern)
        )
        count_stmt = count_stmt.where(
            Article.title.ilike(pattern) | Article.body.ilike(pattern)
        )

    # ── Count ─────────────────────────────────────────
    total_result = await db.execute(count_stmt)
    total = total_result.scalar() or 0

    # ── Sort + paginate ───────────────────────────────
    stmt = (
        stmt.order_by(Article.published_at.desc().nullslast(), Article.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )

    result = await db.execute(stmt)
    articles = result.scalars().unique().all()

    return ArticleListResponse(
        items=[ArticleRead.model_validate(a) for a in articles],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=math.ceil(total / page_size) if total else 0,
    )


@router.get("/{article_id}", response_model=ArticleRead)
async def get_article(
    article_id: str,
    db: AsyncSession = Depends(get_db),
) -> ArticleRead:
    """Get a single article by ID."""
    from uuid import UUID as PyUUID

    from fastapi import HTTPException

    try:
        uid = PyUUID(article_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid article ID format")

    stmt = (
        select(Article)
        .where(Article.id == uid)
        .options(selectinload(Article.categories))
    )
    result = await db.execute(stmt)
    article = result.scalar_one_or_none()

    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")

    return ArticleRead.model_validate(article)


@router.post("/{article_id}/analyze", response_model=ArticleRead)
async def analyze_article(
    article_id: str,
    db: AsyncSession = Depends(get_db),
) -> ArticleRead:
    """Manually trigger full AI analysis (Bias, Summary, SDG) for a specific article."""
    from uuid import UUID as PyUUID

    from fastapi import HTTPException
    
    from app.services.bias_analyzer import analyze_article_bias
    from app.services.nlp_engine import generate_summary, map_sdgs

    try:
        uid = PyUUID(article_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid article ID format")

    stmt = (
        select(Article)
        .where(Article.id == uid)
        .options(selectinload(Article.categories))
    )
    result = await db.execute(stmt)
    article = result.scalar_one_or_none()

    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")

    full_text = f"{article.title}\n\n{article.body or ''}\n\n{article.summary or ''}"

    bias_result = await analyze_article_bias(
        title=article.title,
        body=article.body,
        summary=article.summary,
    )
    ai_summary = await generate_summary(full_text)
    sdg_tags = await map_sdgs(full_text)

    article.bias_score = bias_result.score
    article.bias_label = bias_result.label
    article.ai_summary = ai_summary
    article.sdg_tags = sdg_tags
    
    await db.commit()
    await db.refresh(article)

    return ArticleRead.model_validate(article)
