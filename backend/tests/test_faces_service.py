from uuid import uuid4

import numpy as np
import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.exceptions import FaceVectorNotFoundError
from src.faces.models import FaceVector
from src.faces.schemas import EMBEDDING_BYTES
from src.faces.service import add_face_vector, delete_face_vector, list_face_vectors
from src.users.models import User, UserRole


def _make_embedding() -> bytes:
    return np.random.default_rng(42).random(128, dtype=np.float32).tobytes()


async def _create_user(session: AsyncSession) -> User:
    user = User(
        username=f"user_{uuid4().hex[:12]}",
        email=f"{uuid4().hex[:12]}@example.com",
        password_hash="hash",
        full_name="Test User",
        role=UserRole.USER,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@pytest.mark.asyncio
async def test_list_face_vectors_empty(database_session: AsyncSession) -> None:
    user = await _create_user(database_session)

    total, faces = await list_face_vectors(user.id, database_session)

    assert total == 0
    assert faces == []


@pytest.mark.asyncio
async def test_add_face_vector_stores_embedding(
    database_session: AsyncSession,
) -> None:
    user = await _create_user(database_session)
    embedding = _make_embedding()

    result = await add_face_vector(user.id, embedding, "正面", database_session)

    assert isinstance(result, FaceVector)
    assert result.user_id == user.id
    assert result.embedding == embedding
    assert result.label == "正面"
    assert len(result.embedding) == EMBEDDING_BYTES


@pytest.mark.asyncio
async def test_add_face_vector_null_label(database_session: AsyncSession) -> None:
    user = await _create_user(database_session)
    embedding = _make_embedding()

    result = await add_face_vector(user.id, embedding, None, database_session)

    assert result.user_id == user.id
    assert result.embedding == embedding
    assert result.label is None


@pytest.mark.asyncio
async def test_list_face_vectors_returns_all_for_user(
    database_session: AsyncSession,
) -> None:
    user = await _create_user(database_session)
    other_user = await _create_user(database_session)
    first = await add_face_vector(user.id, _make_embedding(), "正面", database_session)
    second = await add_face_vector(user.id, _make_embedding(), "側面", database_session)
    await add_face_vector(other_user.id, _make_embedding(), "other", database_session)

    total, faces = await list_face_vectors(user.id, database_session)

    assert total == 2
    assert {face.id for face in faces} == {first.id, second.id}


@pytest.mark.asyncio
async def test_delete_face_vector_removes_it(database_session: AsyncSession) -> None:
    user = await _create_user(database_session)
    face = await add_face_vector(user.id, _make_embedding(), "正面", database_session)

    await delete_face_vector(face.id, user.id, database_session)

    total, faces = await list_face_vectors(user.id, database_session)
    assert total == 0
    assert faces == []


@pytest.mark.asyncio
async def test_delete_face_vector_wrong_user_raises(
    database_session: AsyncSession,
) -> None:
    user = await _create_user(database_session)
    other_user = await _create_user(database_session)
    face = await add_face_vector(user.id, _make_embedding(), "正面", database_session)

    with pytest.raises(FaceVectorNotFoundError):
        await delete_face_vector(face.id, other_user.id, database_session)


@pytest.mark.asyncio
async def test_delete_nonexistent_face_vector_raises(
    database_session: AsyncSession,
) -> None:
    user = await _create_user(database_session)

    with pytest.raises(FaceVectorNotFoundError):
        await delete_face_vector(uuid4(), user.id, database_session)
