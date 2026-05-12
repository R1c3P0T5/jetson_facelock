from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel

from src.core.utils import utc_now_naive


class Door(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(unique=True, index=True, nullable=False, max_length=128)
    mqtt_id: str | None = Field(default=None, unique=True, index=True, max_length=64)
    location: str | None = Field(default=None, max_length=256)
    is_active: bool = Field(default=True, nullable=False)
    created_at: datetime = Field(default_factory=utc_now_naive, nullable=False)
