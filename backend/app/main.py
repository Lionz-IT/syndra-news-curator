"""Syndra — FastAPI application entry point."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import health
from app.api.routes import categories as categories_router
from app.api.routes import news as news_router
from app.api.routes import auth as auth_router
from app.api.routes import bookmarks as bookmarks_router
from app.core.config import get_settings
from app.services.worker import start_scheduler, stop_scheduler

logger = logging.getLogger(__name__)


async def _seed_categories() -> None:
    """Upsert category taxonomy on startup (idempotent)."""
    from sqlalchemy import select

    from app.core.database import async_session_factory
    from app.core.seed_categories import CATEGORY_SEED
    from app.models.category import Category

    async with async_session_factory() as session:
        # Check if any categories exist
        result = await session.execute(select(Category).limit(1))
        if result.scalar_one_or_none() is not None:
            logger.info("Categories already seeded — skipping.")
            return

        order = 0
        for entry in CATEGORY_SEED:
            order += 1
            parent = Category(
                name=entry["name"],
                slug=entry["slug"],
                icon=entry.get("icon"),
                color=entry.get("color"),
                description=entry.get("description"),
                display_order=order,
            )
            session.add(parent)
            await session.flush()  # get parent.id

            for child_entry in entry.get("children", []):
                order += 1
                child = Category(
                    name=child_entry["name"],
                    slug=child_entry["slug"],
                    icon=child_entry.get("icon"),
                    color=child_entry.get("color"),
                    description=child_entry.get("description"),
                    display_order=order,
                    parent_id=parent.id,
                )
                session.add(child)

        await session.commit()
        logger.info("Seeded %d category entries.", order)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Startup / shutdown lifecycle hook."""
    try:
        await _seed_categories()
    except Exception:
        logger.warning("Category seeding skipped (DB may not be available yet).", exc_info=True)
        
    # Hidupkan robot pengumpul berita otomatis
    start_scheduler()
    
    yield
    
    # Matikan robot saat server dimatikan
    stop_scheduler()


def create_app() -> FastAPI:
    settings = get_settings()

    # ── Sentry Observability ──────────────────────────────
    if settings.SENTRY_DSN:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            environment=settings.ENVIRONMENT,
            traces_sample_rate=1.0,
        )
        logger.info("Sentry initialized for environment: %s", settings.ENVIRONMENT)

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "AI-powered universal multilingual news curation platform. "
            "Aggregates trustworthy news across every domain worldwide, "
            "detects bias with AI, summarizes articles multilingually, "
            "maps relevant content to UN SDGs, and recommends adaptively."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # ── CORS ──────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Routers ───────────────────────────────────────────
    app.include_router(health.router, prefix="/api")
    app.include_router(categories_router.router, prefix="/api")
    app.include_router(news_router.router, prefix="/api")
    app.include_router(auth_router.router, prefix="/api")
    app.include_router(bookmarks_router.router, prefix="/api")

    return app


app = create_app()
