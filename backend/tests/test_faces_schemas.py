import base64
from datetime import datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError


def test_create_request_decode_embedding_returns_raw_bytes() -> None:
    from src.faces.schemas import EMBEDDING_BYTES, FaceVectorCreateRequest

    encoded = base64.b64encode(b"\0" * EMBEDDING_BYTES).decode()
    request = FaceVectorCreateRequest(embedding=encoded, label="front")

    assert request.embedding == encoded
    assert request.decode_embedding() == b"\0" * 512


def test_create_request_decode_embedding_rejects_invalid_base64() -> None:
    from src.faces.schemas import FaceVectorCreateRequest

    request = FaceVectorCreateRequest(embedding="not base64!!!")
    with pytest.raises(ValueError, match="Invalid base64 encoding"):
        request.decode_embedding()


def test_create_request_decode_embedding_rejects_wrong_byte_size() -> None:
    from src.faces.schemas import FaceVectorCreateRequest

    encoded = base64.b64encode(b"\0" * 4).decode()
    request = FaceVectorCreateRequest(embedding=encoded)

    with pytest.raises(ValueError, match=r"Embedding must be 512 bytes .* got 4"):
        request.decode_embedding()


def test_recognize_request_validates_threshold_bounds_and_default() -> None:
    from src.faces.schemas import EMBEDDING_BYTES, RecognizeRequest

    encoded = base64.b64encode(b"\0" * EMBEDDING_BYTES).decode()

    default_request = RecognizeRequest(embedding=encoded)
    assert default_request.embedding == encoded
    assert default_request.threshold == 0.6
    assert default_request.decode_embedding() == b"\0" * 512
    assert RecognizeRequest(embedding=encoded, threshold=0).threshold == 0
    assert RecognizeRequest(embedding=encoded, threshold=1).threshold == 1

    with pytest.raises(ValidationError):
        RecognizeRequest(embedding=encoded, threshold=-0.1)

    with pytest.raises(ValidationError):
        RecognizeRequest(embedding=encoded, threshold=1.1)


def test_metadata_and_list_response_expose_embedding_size_and_faces() -> None:
    from src.faces.schemas import FaceVectorListResponse, FaceVectorMetadata

    metadata = FaceVectorMetadata(
        id=uuid4(),
        label="front",
        embedding_size=512,
        created_at=datetime(2026, 5, 11),
    )
    response = FaceVectorListResponse(total=1, faces=[metadata])

    assert metadata.embedding_size == 512
    assert response.total == 1
    assert response.faces == [metadata]
