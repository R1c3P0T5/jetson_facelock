from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.config import get_settings


engine: AsyncEngine | None = None
async_session: async_sessionmaker[AsyncSession] | None = None


async def init_db() -> None:
    """Set up async engine and session factory.

    Deferred to avoid calling get_settings() at import time.
    Production schema is managed by Alembic migrations.
    """

    global engine, async_session

    if engine is not None and async_session is not None:
        return

    settings = get_settings()
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        future=True,
    )
    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )


async def create_db_and_tables() -> None:
    """Create all SQLModel tables from metadata.

    For development and testing only — production uses Alembic migrations.
    Safe to call multiple times (create_all is idempotent).
    """

    if engine is None:
        raise RuntimeError("Database is not initialized. Call init_db() first.")

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def close_db() -> None:
    """Dispose the engine and clear the session factory."""

    global engine, async_session
    if engine is None:
        return
    await engine.dispose()
    engine = None
    async_session = None


@asynccontextmanager
async def session_context() -> AsyncGenerator[AsyncSession, None]:
    """Context manager that yields a session; for use outside request handling."""

    if async_session is None:
        raise RuntimeError("Database is not initialized. Call init_db() first.")

    async with async_session() as session:
        yield session


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield an async database session (FastAPI dependency)."""

    if async_session is None:
        raise RuntimeError("Database is not initialized. Call init_db() first.")

    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
