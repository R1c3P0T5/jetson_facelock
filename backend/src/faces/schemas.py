from base64 import b64decode
from binascii import Error as Base64DecodeError
from datetime import datetime
from uuid import UUID

import numpy as np
from pydantic import BaseModel, ConfigDict, Field


EMBEDDING_DIM = 128
EMBEDDING_BYTES = EMBEDDING_DIM * np.dtype(np.float32).itemsize


def _decode_embedding(b64: str) -> bytes:
    try:
        data = b64decode(b64, validate=True)
    except (Base64DecodeError, ValueError) as exc:
        raise ValueError("Invalid base64 encoding") from exc

    if len(data) != EMBEDDING_BYTES:
        raise ValueError(
            f"Embedding must be {EMBEDDING_BYTES} bytes "
            f"({EMBEDDING_DIM} × float32), got {len(data)}"
        )

    return data


class FaceVectorCreateRequest(BaseModel):
    """Request to create a face vector for a user."""

    embedding: str = Field(
        ...,
        min_length=1,
        description="Base64-encoded 128-dimensional float32 embedding.",
    )
    label: str | None = Field(
        default=None,
        max_length=64,
    )

    def decode_embedding(self) -> bytes:
        return _decode_embedding(self.embedding)


class FaceVectorMetadata(BaseModel):
    """Face vector metadata without raw embedding bytes."""

    id: UUID = Field(description="Stable face vector identifier.")
    label: str | None = Field(default=None, description="Optional face vector label.")
    embedding_size: int = Field(description="Stored embedding size in bytes.")
    created_at: datetime = Field(
        description="UTC timestamp when the vector was created."
    )

    model_config = ConfigDict(from_attributes=True)


class FaceVectorListResponse(BaseModel):
    """List response for face vector metadata."""

    total: int = Field(description="Total number of face vectors.")
    faces: list[FaceVectorMetadata] = Field(description="Face vectors.")


class RecognizeRequest(BaseModel):
    """Request to recognize a face embedding."""

    embedding: str = Field(
        ...,
        min_length=1,
        description="Base64-encoded 128-dimensional float32 embedding.",
    )
    threshold: float = Field(
        default=0.6,
        ge=0.0,
        le=1.0,
        description="Minimum confidence threshold for a match.",
    )

    def decode_embedding(self) -> bytes:
        return _decode_embedding(self.embedding)


class RecognizeResponse(BaseModel):
    """Response for a face recognition attempt."""

    matched: bool = Field(description="Whether a face vector matched the request.")
    user_id: UUID | None = Field(default=None, description="Matched user identifier.")
    username: str | None = Field(default=None, description="Matched username.")
    confidence: float = Field(description="Recognition confidence score.")
