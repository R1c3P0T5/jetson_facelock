from collections.abc import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.core.database import async_session, close_db, engine, get_session, init_db


def test_database_engine_uses_configured_async_sqlite_url() -> None:
    assert isinstance(engine, AsyncEngine)
    assert str(engine.url) == "sqlite+aiosqlite:///./jetson_facelock.db"
    assert async_session.kw["expire_on_commit"] is False


@pytest.mark.asyncio
async def test_get_session_yields_async_session() -> None:
    session_generator = get_session()

    assert isinstance(session_generator, AsyncGenerator)

    session = await anext(session_generator)
    try:
        assert isinstance(session, AsyncSession)
    finally:
        await session_generator.aclose()


@pytest.mark.asyncio
async def test_init_and_close_db_are_awaitable() -> None:
    assert await init_db() is None
    assert await close_db() is None
