"""Application configuration via environment variables."""

from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central config — all values read from env / .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── App ───────────────────────────────────────────────
    APP_NAME: str = "Syndra"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"

    # ── Server ────────────────────────────────────────────
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ── CORS ──────────────────────────────────────────────
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]

    # ── Database ──────────────────────────────────────────
    DATABASE_URL: str = "postgresql+asyncpg://syndra:syndra@localhost:5432/syndra"

    # ── Redis ─────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"

    # ── JWT / Auth ────────────────────────────────────────
    SECRET_KEY: str = "CHANGE-ME-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # ── External API keys (all optional — mock fallback) ─
    NEWSAPI_KEY: str = ""
    GUARDIAN_API_KEY: str = ""
    GNEWS_API_KEY: str = ""
    NYT_API_KEY: str = ""
    MEDIASTACK_API_KEY: str = ""
    CURRENTS_API_KEY: str = ""
    WORLDBANK_API_KEY: str = ""
    HF_API_TOKEN: str = ""

    # ── Sentry (optional) ────────────────────────────────
    SENTRY_DSN: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
