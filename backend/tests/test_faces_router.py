import base64
from uuid import uuid4

import numpy as np
import pytest
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.utils import create_access_token, hash_password
from src.users.models import User, UserRole


def _make_b64_embedding(seed: int = 0) -> str:
    embedding = np.random.default_rng(seed).random(128, dtype=np.float32)
    return base64.b64encode(embedding.tobytes()).decode()


async def _create_user_with_token(
    session: AsyncSession,
    *,
    role: UserRole = UserRole.USER,
) -> tuple[User, str]:
    user = User(
        username=f"user_{uuid4().hex[:12]}",
        email=f"{uuid4().hex[:12]}@example.com",
        password_hash=hash_password("Pass123!"),
        full_name="Face Router User",
        role=role,
        is_active=True,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user, create_access_token(user.id)


def _auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_list_faces_empty_returns_total_and_faces(
    client: AsyncClient,
    database_session: AsyncSession,
) -> None:
    user, token = await _create_user_with_token(database_session)

    response = await client.get(
        f"/api/users/{user.id}/faces",
        headers=_auth_headers(token),
    )

    assert response.status_code == 200
    assert response.json() == {"total": 0, "faces": []}


@pytest.mark.asyncio
async def test_list_faces_requires_authentication(
    client: AsyncClient,
    database_session: AsyncSession,
) -> None:
    user, _ = await _create_user_with_token(database_session)

    response = await client.get(f"/api/users/{user.id}/faces")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_list_faces_forbids_other_user(
    client: AsyncClient,
    database_session: AsyncSession,
) -> None:
    user, _ = await _create_user_with_token(database_session)
    other_user, other_token = await _create_user_with_token(database_session)

    response = await client.get(
        f"/api/users/{user.id}/faces",
        headers=_auth_headers(other_token),
    )

    assert other_user.id != user.id
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_admin_can_list_faces_for_any_user(
    client: AsyncClient,
    database_session: AsyncSession,
) -> None:
    user, _ = await _create_user_with_token(database_session)
    _, admin_token = await _create_user_with_token(
        database_session,
        role=UserRole.ADMIN,
    )

    response = await client.get(
        f"/api/users/{user.id}/faces",
        headers=_auth_headers(admin_token),
    )

    assert response.status_code == 200
    assert response.json() == {"total": 0, "faces": []}


@pytest.mark.asyncio
async def test_create_face_with_valid_embedding_returns_metadata(
    client: AsyncClient,
    database_session: AsyncSession,
) -> None:
    user, token = await _create_user_with_token(database_session)

    response = await client.post(
        f"/api/users/{user.id}/faces",
        json={"embedding": _make_b64_embedding(), "label": "正面"},
        headers=_auth_headers(token),
    )

    assert response.status_code == 201
    data = response.json()
    assert data["embedding_size"] == 512
    assert data["label"] == "正面"
    assert data["id"]
    assert data["created_at"]


@pytest.mark.asyncio
async def test_create_face_rejects_short_embedding(
    client: AsyncClient,
    database_session: AsyncSession,
) -> None:
    user, token = await _create_user_with_token(database_session)
    short_embedding = base64.b64encode(
        np.array([1.0], dtype=np.float32).tobytes()
    ).decode()

    response = await client.post(
        f"/api/users/{user.id}/faces",
        json={"embedding": short_embedding, "label": "正面"},
        headers=_auth_headers(token),
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_face_rejects_bad_base64(
    client: AsyncClient,
    database_session: AsyncSession,
) -> None:
    user, token = await _create_user_with_token(database_session)

    response = await client.post(
        f"/api/users/{user.id}/faces",
        json={"embedding": "not base64!!!", "label": "正面"},
        headers=_auth_headers(token),
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_delete_face_returns_no_content_after_adding(
    client: AsyncClient,
    database_session: AsyncSession,
) -> None:
    user, token = await _create_user_with_token(database_session)
    create_response = await client.post(
        f"/api/users/{user.id}/faces",
        json={"embedding": _make_b64_embedding(), "label": "正面"},
        headers=_auth_headers(token),
    )
    assert create_response.status_code == 201
    face_id = create_response.json()["id"]

    response = await client.delete(
        f"/api/users/{user.id}/faces/{face_id}",
        headers=_auth_headers(token),
    )

    assert response.status_code == 204
    assert response.content == b""


@pytest.mark.asyncio
async def test_delete_nonexistent_face_returns_not_found(
    client: AsyncClient,
    database_session: AsyncSession,
) -> None:
    user, token = await _create_user_with_token(database_session)

    response = await client.delete(
        f"/api/users/{user.id}/faces/{uuid4()}",
        headers=_auth_headers(token),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Face vector not found"


@pytest.mark.asyncio
async def test_recognize_valid_embedding_returns_unmatched_response(
    client: AsyncClient,
) -> None:
    response = await client.post(
        "/api/faces/recognize",
        json={"embedding": _make_b64_embedding()},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["matched"] is False
    assert data["user_id"] is None
    assert data["username"] is None
    assert isinstance(data["confidence"], float)


@pytest.mark.asyncio
async def test_recognize_rejects_invalid_embedding(client: AsyncClient) -> None:
    response = await client.post(
        "/api/faces/recognize",
        json={"embedding": "not base64!!!"},
    )

    assert response.status_code == 400
