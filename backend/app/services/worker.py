"""Background worker — scheduled news aggregation via APScheduler."""

from __future__ import annotations

import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.core.database import async_session_factory
from app.services.aggregator import fetch_all_sources, persist_articles

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def aggregate_news_job() -> None:
    """Scheduled job: fetch from all adapters, dedupe, persist."""
    logger.info("Starting scheduled news aggregation...")

    try:
        articles = await fetch_all_sources()
        async with async_session_factory() as session:
            inserted = await persist_articles(session, articles)
            await session.commit()
            logger.info("Aggregation complete: %d new articles persisted.", inserted)
    except Exception:
        logger.exception("Aggregation job failed.")


def start_scheduler() -> None:
    """Start the APScheduler with the aggregation job."""
    scheduler.add_job(
        aggregate_news_job,
        trigger="interval",
        minutes=15,
        id="aggregate_news",
        replace_existing=True,
        max_instances=1,
    )
    scheduler.start()
    logger.info("Scheduler started — aggregation every 15 minutes.")


def stop_scheduler() -> None:
    """Gracefully stop the scheduler."""
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Scheduler stopped.")
