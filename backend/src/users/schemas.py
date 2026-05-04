from base64 import b64decode
from binascii import Error as Base64DecodeError
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.users.models import UserRole


MAX_FACE_EMBEDDING_SIZE = 2 * 1024 * 1024


class UserUpdateRequest(BaseModel):
    """User profile update request."""

    full_name: str | None = Field(
        None,
        max_length=255,
        description="Optional replacement display name.",
        examples=["Updated Operator"],
    )
    email: EmailStr | None = Field(
        default=None,
        description="Optional replacement email address.",
        examples=["updated.operator@example.com"],
    )


class UserFaceEmbeddingUpdateRequest(BaseModel):
    """Base64 encoded face embedding update request."""

    face_embedding: str = Field(
        ...,
        min_length=1,
        description=(
            "Base64-encoded face embedding bytes. The decoded payload must not "
            "exceed 2 MiB."
        ),
        examples=["ZmFjZS1lbWJlZGRpbmctYnl0ZXM="],
    )

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

    id: UUID = Field(description="Stable user identifier.")
    username: str = Field(description="Unique login name.")
    face_embedding_size: int = Field(
        ...,
        ge=0,
        description="Stored face embedding size in bytes.",
    )


class UserResponseFull(BaseModel):
    """Full user information for admin responses."""

    id: UUID = Field(description="Stable user identifier.")
    username: str = Field(description="Unique login name.")
    email: str | None = Field(default=None, description="Optional email address.")
    full_name: str = Field(description="Human-readable display name.")
    role: UserRole = Field(description="Authorization role assigned to the user.")
    is_active: bool = Field(description="Whether the account can authenticate.")
    created_at: datetime = Field(description="UTC timestamp when the user was created.")
    updated_at: datetime = Field(
        description="UTC timestamp for the latest profile change."
    )
    face_embedding_size: int = Field(
        ...,
        ge=0,
        description="Stored face embedding size in bytes.",
    )

    model_config = ConfigDict(from_attributes=True)


class UserListResponse(BaseModel):
    """Paginated user list response."""

    total: int = Field(..., ge=0, description="Total users matching the query.")
    skip: int = Field(..., ge=0, description="Number of skipped users.")
    limit: int = Field(..., ge=1, description="Maximum users requested.")
    users: list[UserResponseFull] = Field(description="Users in the current page.")
