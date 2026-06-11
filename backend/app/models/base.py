"""Declarative base for all SQLAlchemy models."""

from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Shared base — all models inherit from this."""
    pass
