from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """User database model for authentication and profile management."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(unique=True, index=True, nullable=False)
    email: str | None = Field(default=None, unique=True, index=True)
    password_hash: str = Field(nullable=False)
    full_name: str = Field(nullable=False)
    face_embedding: bytes | None = None
    role: str = Field(default="user", nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
