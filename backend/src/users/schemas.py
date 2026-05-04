from base64 import b64decode
from binascii import Error as Base64DecodeError
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.users.models import UserRole


MAX_FACE_EMBEDDING_SIZE = 2 * 1024 * 1024


class UserUpdateRequest(BaseModel):
    """User profile update request."""

    full_name: str | None = Field(None, max_length=255)
    email: EmailStr | None = None


class UserFaceEmbeddingUpdateRequest(BaseModel):
    """Base64 encoded face embedding update request."""

    face_embedding: str = Field(..., min_length=1)

    def validate_and_decode(self) -> bytes:
        try:
            embedding = b64decode(self.face_embedding, validate=True)
        except (Base64DecodeError, ValueError) as exc:
            raise ValueError("Invalid face embedding base64 data") from exc
        if len(embedding) > MAX_FACE_EMBEDDING_SIZE:
            raise ValueError(
                "Face embedding too large: "
                f"{len(embedding)} bytes > {MAX_FACE_EMBEDDING_SIZE} bytes"
            )
        return embedding


class UserFaceEmbeddingResponse(BaseModel):
    """Face embedding response metadata."""

    id: UUID
    username: str
    face_embedding_size: int = Field(..., ge=0)


class UserResponseFull(BaseModel):
    """Full user information for admin responses."""

    id: UUID
    username: str
    email: str | None = None
    full_name: str
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime
    face_embedding_size: int = Field(..., ge=0)

    model_config = ConfigDict(from_attributes=True)


class UserListResponse(BaseModel):
    """Paginated user list response."""

    total: int = Field(..., ge=0)
    skip: int = Field(..., ge=0)
    limit: int = Field(..., ge=1)
    users: list[UserResponseFull]
