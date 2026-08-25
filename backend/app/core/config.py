"""Environment-backed configuration for the database foundation."""

from __future__ import annotations

import os


def get_database_url() -> str:
    """Return the required PostgreSQL connection URL without exposing a default."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is required, for example: "
            "postgresql+psycopg://username:password@localhost:5432/coinly"
        )
    if not database_url.startswith("postgresql+"):
        raise RuntimeError("DATABASE_URL must use a PostgreSQL SQLAlchemy dialect.")
    return database_url
