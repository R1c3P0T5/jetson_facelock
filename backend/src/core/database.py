from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel import SQLModel

from src.core.config import get_settings


engine: AsyncEngine | None = None
async_session: async_sessionmaker[AsyncSession] | None = None


async def init_db() -> None:
    """Initialize DB engine/session.

    Production schema is managed by Alembic; this only ensures connectivity.
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

    _ = SQLModel.metadata


async def close_db() -> None:
    """Close database connections."""

    global engine, async_session
    if engine is None:
        return
    await engine.dispose()
    engine = None
    async_session = None


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency function to inject a database session into routes."""

    if async_session is None:
        raise RuntimeError("Database is not initialized. Call init_db() first.")

    async with async_session() as session:
        yield session
