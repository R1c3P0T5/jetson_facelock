from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from main import app
from src.auth.utils import hash_password
from src.core.database import get_session
from src.users.models import User, UserRole


@pytest_asyncio.fixture
async def engine() -> AsyncGenerator[AsyncEngine, None]:
    test_engine = create_async_engine(
        "sqlite+aiosqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    try:
        yield test_engine
    finally:
        await test_engine.dispose()


@pytest_asyncio.fixture
async def database_session(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(
        engine,
        expire_on_commit=False,
        autoflush=False,
    ) as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def client(
    database_session: AsyncSession,
) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
        yield database_session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as async_client:
        yield async_client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(database_session: AsyncSession) -> User:
    user = User(
        username="testuser",
        email="testuser@example.com",
        password_hash=hash_password("TestPassword123"),
        full_name="Test User",
        role=UserRole.USER,
        is_active=True,
    )
    database_session.add(user)
    await database_session.commit()
    await database_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def test_admin(database_session: AsyncSession) -> User:
    admin = User(
        username="admin",
        email="admin@example.com",
        password_hash=hash_password("AdminPassword123"),
        full_name="Admin User",
        role=UserRole.ADMIN,
        is_active=True,
    )
    database_session.add(admin)
    await database_session.commit()
    await database_session.refresh(admin)
    return admin


@pytest.fixture(autouse=True)
def clear_dependency_overrides() -> Generator[None, None, None]:
    try:
        yield
    finally:
        app.dependency_overrides.clear()
