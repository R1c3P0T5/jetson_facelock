from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from src.core.config import settings


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


async def init_db() -> None:
    """Initialize database tables for tests only; production uses Alembic."""

    _ = SQLModel.metadata


async def close_db() -> None:
    """Close database connections."""

    await engine.dispose()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency function to inject a database session into routes."""

    async with async_session() as session:
        yield session
