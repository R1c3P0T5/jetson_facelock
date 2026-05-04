from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlmodel.ext.asyncio.session import AsyncSession

import src.core.database as db


@pytest_asyncio.fixture
async def database_session() -> AsyncGenerator[AsyncSession, None]:
    await db.init_db()
    await db.create_db_and_tables()

    assert db.async_session is not None
    async with db.async_session() as session:
        try:
            yield session
        finally:
            await db.close_db()
