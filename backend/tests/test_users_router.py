from uuid import uuid4

import pytest
from fastapi.routing import APIRoute
from sqlmodel.ext.asyncio.session import AsyncSession

from src.users.models import User, UserRole, UserStatus
from src.users.schemas import (
    UserListResponse,
    UserUpdateRequest,
)


async def create_user(
    session: AsyncSession,
    *,
    role: UserRole = UserRole.USER,
    status: UserStatus = UserStatus.APPROVED,
) -> User:
    user = User(
        username=f"user_{uuid4().hex[:12]}",
        email=f"{uuid4().hex[:12]}@example.com",
        password_hash="hash",
        full_name="Router User",
        role=role,
        status=status,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


def test_users_router_exposes_expected_routes() -> None:
    from src.users.router import router

    routes = {
        (route.path, tuple(sorted(route.methods or [])))
        for route in router.routes
        if isinstance(route, APIRoute)
    }

    assert router.prefix == "/api/users"
    assert ("/api/users", ("GET",)) in routes
    assert ("/api/users/{user_id}/approve", ("POST",)) in routes
    assert ("/api/users/{user_id}/reject", ("POST",)) in routes
    assert ("/api/users/{user_id}", ("GET",)) in routes
    assert ("/api/users/{user_id}", ("PUT",)) in routes
    assert ("/api/users/{user_id}", ("DELETE",)) in routes


def test_main_app_includes_users_routes() -> None:
    from main import app

    routes = {
        (route.path, tuple(sorted(route.methods or [])))
        for route in app.routes
        if isinstance(route, APIRoute)
    }

    assert ("/api/users", ("GET",)) in routes
    assert ("/api/users/{user_id}", ("GET",)) in routes


@pytest.mark.asyncio
async def test_get_user_endpoint_returns_user_response(
    database_session: AsyncSession,
) -> None:
    from src.users.router import get_user

    user = await create_user(database_session)

    response = await get_user(user.id, database_session, user)

    assert response.id == user.id
    assert response.username == user.username
    assert response.status == UserStatus.APPROVED


@pytest.mark.asyncio
async def test_update_user_endpoint_returns_updated_user(
    database_session: AsyncSession,
) -> None:
    from src.users.router import update_user_profile

    user = await create_user(database_session)

    response = await update_user_profile(
        user.id,
        UserUpdateRequest(full_name="Updated User"),
        database_session,
        user,
    )

    assert response.full_name == "Updated User"


@pytest.mark.asyncio
async def test_delete_user_endpoint_returns_none(
    database_session: AsyncSession,
) -> None:
    from src.users.router import delete_user_profile

    user = await create_user(database_session)

    assert await delete_user_profile(user.id, database_session, user) is None


@pytest.mark.asyncio
async def test_list_users_endpoint_returns_paginated_response(
    database_session: AsyncSession,
) -> None:
    from src.users.router import list_users_endpoint

    admin = await create_user(database_session, role=UserRole.ADMIN)
    await create_user(database_session)

    response = await list_users_endpoint(database_session, admin, skip=0, limit=50)

    assert isinstance(response, UserListResponse)
    assert response.total >= 2
    assert response.limit == 50
    assert {user.status for user in response.users} == {UserStatus.APPROVED}


@pytest.mark.asyncio
async def test_list_users_endpoint_filters_by_status(
    database_session: AsyncSession,
) -> None:
    from src.users.router import list_users_endpoint

    admin = await create_user(database_session, role=UserRole.ADMIN)
    pending_user = await create_user(database_session, status=UserStatus.PENDING)
    await create_user(database_session, status=UserStatus.APPROVED)

    response = await list_users_endpoint(
        database_session, admin, skip=0, limit=50, status=UserStatus.PENDING
    )

    assert isinstance(response, UserListResponse)
    assert response.total == 1
    assert response.users[0].id == pending_user.id
    assert response.users[0].status == UserStatus.PENDING


@pytest.mark.asyncio
async def test_approve_user_endpoint_returns_approved_response(
    database_session: AsyncSession,
) -> None:
    from src.users.router import approve_user_endpoint

    admin = await create_user(database_session, role=UserRole.ADMIN)
    pending_user = await create_user(database_session, status=UserStatus.PENDING)

    response = await approve_user_endpoint(pending_user.id, database_session, admin)

    assert response.id == pending_user.id
    assert response.status == UserStatus.APPROVED


@pytest.mark.asyncio
async def test_reject_user_endpoint_returns_rejected_response(
    database_session: AsyncSession,
) -> None:
    from src.users.router import reject_user_endpoint

    admin = await create_user(database_session, role=UserRole.ADMIN)
    pending_user = await create_user(database_session, status=UserStatus.PENDING)

    response = await reject_user_endpoint(pending_user.id, database_session, admin)

    assert response.id == pending_user.id
    assert response.status == UserStatus.REJECTED
