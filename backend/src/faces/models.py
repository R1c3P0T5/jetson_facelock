from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


def _utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class FaceVector(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True, nullable=False)
    embedding: bytes = Field(nullable=False)
    label: str | None = Field(default=None, max_length=64)
    created_at: datetime = Field(default_factory=_utc_now, nullable=False)
