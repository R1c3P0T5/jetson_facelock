from datetime import datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError


def test_user_register_request_validates_required_fields() -> None:
    from src.auth.schemas import UserRegisterRequest

    request = UserRegisterRequest(
        username="john_doe",
        password="MySecurePass123",
        full_name="John Doe",
        email="john@example.com",
    )

    assert request.username == "john_doe"
    assert request.email == "john@example.com"


def test_user_register_request_rejects_short_password() -> None:
    from src.auth.schemas import UserRegisterRequest

    with pytest.raises(ValidationError):
        UserRegisterRequest(
            username="john_doe",
            password="short",
            full_name="John Doe",
        )


def test_login_response_defaults_token_type_to_bearer() -> None:
    from src.auth.schemas import LoginResponse, UserResponse

    user = UserResponse(
        id=uuid4(),
        username="john_doe",
        full_name="John Doe",
        role="user",
        is_active=True,
        created_at=datetime.now(),
    )

    response = LoginResponse(access_token="token", user=user)

    assert response.token_type == "bearer"
    assert response.user.username == "john_doe"


def test_user_update_request_allows_partial_update() -> None:
    from src.auth.schemas import UserUpdateRequest

    request = UserUpdateRequest(full_name="Jane Doe")

    assert request.full_name == "Jane Doe"
    assert request.email is None


def test_user_face_update_request_validates_max_size() -> None:
    from src.auth.schemas import UserFaceUpdateRequest

    request = UserFaceUpdateRequest(face_embedding=b"abc")
    assert len(request.face_embedding) == 3

    with pytest.raises(ValidationError, match="Face embedding too large"):
        UserFaceUpdateRequest(face_embedding=b"x" * (2 * 1024 * 1024 + 1))


def test_user_face_response_exposes_embedding_size() -> None:
    from src.auth.schemas import UserFaceResponse

    response = UserFaceResponse(
        id=uuid4(), username="john_doe", face_embedding_size=128
    )

    assert response.face_embedding_size == 128
