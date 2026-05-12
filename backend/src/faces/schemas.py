from base64 import b64decode
from binascii import Error as Base64DecodeError
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


EMBEDDING_DIM = 128
EMBEDDING_BYTES = 512  # 128 × float32 (4 bytes each)


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


class _EmbeddingRequest(BaseModel):
    embedding: str = Field(
        ...,
        min_length=1,
        description="Base64-encoded 128-dimensional float32 embedding.",
    )

    def decode_embedding(self) -> bytes:
        return _decode_embedding(self.embedding)


class FaceVectorCreateRequest(_EmbeddingRequest):
    label: str | None = Field(default=None, min_length=1, max_length=64)


class FaceVectorMetadata(BaseModel):
    """Face vector metadata — does not expose raw embedding bytes."""

    id: UUID = Field(description="Stable face vector identifier.")
    label: str | None = Field(default=None, description="Optional face vector label.")
    embedding_size: int = Field(description="Stored embedding size in bytes.")
    created_at: datetime = Field(
        description="UTC timestamp when the vector was created."
    )


class FaceVectorListResponse(BaseModel):
    total: int = Field(description="Total number of face vectors stored.")
    skip: int = Field(description="Number of face vectors skipped.")
    limit: int = Field(description="Maximum face vectors requested.")
    faces: list[FaceVectorMetadata] = Field(description="Face vectors.")


class RecognizeRequest(_EmbeddingRequest):
    threshold: float = Field(
        default=0.363,
        ge=0.0,
        le=1.0,
        description="Minimum cosine similarity threshold for a match.",
    )


class RecognizeResponse(BaseModel):
    matched: bool = Field(description="Whether a face vector matched the request.")
    user_id: UUID | None = Field(default=None, description="Matched user identifier.")
    username: str | None = Field(default=None, description="Matched username.")
    confidence: float = Field(description="Recognition confidence score.")
