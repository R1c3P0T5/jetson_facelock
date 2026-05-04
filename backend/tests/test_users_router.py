from base64 import b64encode
from uuid import uuid4

import pytest
from fastapi.routing import APIRoute
from sqlmodel.ext.asyncio.session import AsyncSession

from src.users.models import User, UserRole
from src.users.schemas import (
    UserFaceEmbeddingResponse,
    UserFaceEmbeddingUpdateRequest,
    UserListResponse,
    UserUpdateRequest,
)


async def create_user(
    session: AsyncSession,
    *,
    role: UserRole = UserRole.USER,
    face_embedding: bytes | None = None,
) -> User:
    user = User(
        username=f"user_{uuid4().hex[:12]}",
        email=f"{uuid4().hex[:12]}@example.com",
        password_hash="hash",
        full_name="Router User",
        role=role,
        face_embedding=face_embedding,
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
    assert ("/api/users/{user_id}", ("GET",)) in routes
    assert ("/api/users/{user_id}", ("PUT",)) in routes
    assert ("/api/users/{user_id}", ("DELETE",)) in routes
    assert ("/api/users/{user_id}/face", ("GET",)) in routes
    assert ("/api/users/{user_id}/face", ("PUT",)) in routes


def test_main_app_includes_users_routes() -> None:
    from main import app

    routes = {
        (route.path, tuple(sorted(route.methods or [])))
        for route in app.routes
        if isinstance(route, APIRoute)
    }

    assert ("/api/users", ("GET",)) in routes
    assert ("/api/users/{user_id}", ("GET",)) in routes
    assert ("/api/users/{user_id}/face", ("PUT",)) in routes


@pytest.mark.asyncio
async def test_get_user_endpoint_returns_user_response(
    database_session: AsyncSession,
) -> None:
    from src.users.router import get_user

    user = await create_user(database_session)

    response = await get_user(user.id, database_session, user)

    assert response.id == user.id
    assert response.username == user.username


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
async def test_update_face_endpoint_decodes_base64_and_returns_size(
    database_session: AsyncSession,
) -> None:
    from src.users.router import update_user_face

    user = await create_user(database_session)
    embedding = b"face-bytes"

    response = await update_user_face(
        user.id,
        UserFaceEmbeddingUpdateRequest(
            face_embedding=b64encode(embedding).decode("ascii")
        ),
        database_session,
        user,
    )

    assert isinstance(response, UserFaceEmbeddingResponse)
    assert response.face_embedding_size == len(embedding)


@pytest.mark.asyncio
async def test_update_face_endpoint_rejects_invalid_base64(
    database_session: AsyncSession,
) -> None:
    from src.core.exceptions import InvalidFaceEmbeddingError
    from src.users.router import update_user_face

    user = await create_user(database_session)

    with pytest.raises(InvalidFaceEmbeddingError) as exc_info:
        await update_user_face(
            user.id,
            UserFaceEmbeddingUpdateRequest(face_embedding="not base64"),
            database_session,
            user,
        )

    assert exc_info.value.status_code == 400


@pytest.mark.asyncio
async def test_get_face_endpoint_returns_existing_size(
    database_session: AsyncSession,
) -> None:
    from src.users.router import get_user_face

    embedding = b"face-bytes"
    user = await create_user(database_session, face_embedding=embedding)

    response = await get_user_face(user.id, database_session, user)

    assert response.face_embedding_size == len(embedding)


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
