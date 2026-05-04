from base64 import b64encode
from datetime import datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError

from src.users.models import UserRole


def test_user_update_request_allows_partial_profile_update() -> None:
    from src.users.schemas import UserUpdateRequest

    request = UserUpdateRequest(full_name="Jane Doe")

    assert request.full_name == "Jane Doe"
    assert request.email is None


def test_user_face_embedding_update_request_decodes_base64() -> None:
    from src.users.schemas import UserFaceEmbeddingUpdateRequest

    embedding = b"face-vector-bytes"
    request = UserFaceEmbeddingUpdateRequest(
        face_embedding=b64encode(embedding).decode("ascii")
    )

    assert request.validate_and_decode() == embedding


def test_user_face_embedding_update_request_rejects_invalid_base64() -> None:
    from src.users.schemas import UserFaceEmbeddingUpdateRequest

    request = UserFaceEmbeddingUpdateRequest(face_embedding="not base64")

    with pytest.raises(ValueError, match="Invalid face embedding"):
        request.validate_and_decode()


def test_user_face_embedding_update_request_rejects_large_payload() -> None:
    from src.users.schemas import UserFaceEmbeddingUpdateRequest

    request = UserFaceEmbeddingUpdateRequest(
        face_embedding=b64encode(b"x" * (2 * 1024 * 1024 + 1)).decode("ascii")
    )

    with pytest.raises(ValueError, match="Face embedding too large"):
        request.validate_and_decode()


def test_user_face_embedding_response_contains_size() -> None:
    from src.users.schemas import UserFaceEmbeddingResponse

    response = UserFaceEmbeddingResponse(
        id=uuid4(),
        username="john_doe",
        face_embedding_size=128,
    )

    assert response.face_embedding_size == 128


def test_user_list_response_wraps_users_and_pagination() -> None:
    from src.users.schemas import UserListResponse, UserResponseFull

    user = UserResponseFull(
        id=uuid4(),
        username="admin",
        email="admin@example.com",
        full_name="Admin User",
        role=UserRole.ADMIN,
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        face_embedding_size=0,
    )

    response = UserListResponse(total=1, skip=0, limit=10, users=[user])

    assert response.total == 1
    assert response.users[0].role == UserRole.ADMIN


def test_user_response_full_rejects_negative_face_embedding_size() -> None:
    from src.users.schemas import UserResponseFull

    with pytest.raises(ValidationError):
        UserResponseFull(
            id=uuid4(),
            username="user",
            full_name="User",
            role=UserRole.USER,
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            face_embedding_size=-1,
        )
