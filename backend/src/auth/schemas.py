from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRegisterRequest(BaseModel):
    """User registration request."""

    username: str = Field(..., min_length=3, max_length=32)
    password: str = Field(..., min_length=12)
    full_name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr | None = None


class UserLoginRequest(BaseModel):
    """User login request."""

    username: str
    password: str


class UserResponse(BaseModel):
    """Safe user data for API responses."""

    id: UUID
    username: str
    email: str | None = None
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LoginResponse(BaseModel):
    """Login response with JWT access token."""

    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class UserUpdateRequest(BaseModel):
    """User profile update request."""

    full_name: str | None = Field(None, max_length=255)
    email: EmailStr | None = None


class UserFaceUpdateRequest(BaseModel):
    """Face embedding update request."""

    face_embedding: bytes

    def validate_size(self) -> None:
        max_size = 2 * 1024 * 1024
        if len(self.face_embedding) > max_size:
            raise ValueError(
                "Face embedding too large: "
                f"{len(self.face_embedding)} bytes > {max_size} bytes"
            )


class UserFaceResponse(BaseModel):
    """Face embedding response."""

    id: UUID
    username: str
    face_embedding_size: int
