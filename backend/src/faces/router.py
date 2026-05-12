from typing import Annotated
from uuid import UUID

import cv2
import numpy as np
from fastapi import APIRouter, Depends, Form, Path, Query, UploadFile, status

from src.auth.dependencies import get_current_user
from src.core.access import require_self_or_admin
from src.core.database import SessionDep
from src.core.exceptions import (
    InvalidFaceVectorError,
    InvalidImageError,
    NoFaceDetectedError,
)
from src.faces.engine import EngineDep
from src.faces.models import FaceVector
from src.faces.schemas import (
    FaceVectorCreateRequest,
    FaceVectorListResponse,
    FaceVectorMetadata,
    RecognizeRequest,
    RecognizeResponse,
)
from src.faces.service import (
    MAX_FACE_VECTORS_PER_USER,
    add_face_vector,
    delete_face_vector,
    list_face_vectors,
)
from src.users.models import User


router = APIRouter(tags=["faces"])


def _to_metadata(face: FaceVector) -> FaceVectorMetadata:
    return FaceVectorMetadata(
        id=face.id,
        label=face.label,
        embedding_size=len(face.embedding),
        created_at=face.created_at,
    )


def _decode_image(data: bytes) -> np.ndarray:
    arr = np.frombuffer(data, dtype=np.uint8)
    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if image is None:
        raise InvalidImageError()
    return image


@router.get(
    "/api/users/{user_id}/faces",
    response_model=FaceVectorListResponse,
    summary="List face vectors",
)
async def list_user_face_vectors(
    user_id: Annotated[UUID, Path(description="User ID whose face vectors to list.")],
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)],
    skip: Annotated[
        int,
        Query(
            ge=0, description="Number of face vectors to skip before returning results."
        ),
    ] = 0,
    limit: Annotated[
        int,
        Query(
            ge=1,
            le=MAX_FACE_VECTORS_PER_USER,
            description="Maximum number of face vectors to return.",
        ),
    ] = MAX_FACE_VECTORS_PER_USER,
) -> FaceVectorListResponse:
    require_self_or_admin(current_user, user_id)
    total, faces = await list_face_vectors(user_id, session, skip=skip, limit=limit)
    return FaceVectorListResponse(
        total=total,
        skip=skip,
        limit=limit,
        faces=[_to_metadata(face) for face in faces],
    )


@router.post(
    "/api/users/{user_id}/faces",
    response_model=FaceVectorMetadata,
    status_code=status.HTTP_201_CREATED,
    summary="Add a face vector",
)
async def add_user_face_vector(
    user_id: Annotated[UUID, Path(description="User ID to attach the face vector to.")],
    request: FaceVectorCreateRequest,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)],
) -> FaceVectorMetadata:
    require_self_or_admin(current_user, user_id)
    try:
        embedding = request.decode_embedding()
    except ValueError as exc:
        raise InvalidFaceVectorError(detail=str(exc)) from exc

    face = await add_face_vector(user_id, embedding, request.label, session)
    return _to_metadata(face)


@router.delete(
    "/api/users/{user_id}/faces/{face_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a face vector",
)
async def delete_user_face_vector(
    user_id: Annotated[UUID, Path(description="User ID that owns the face vector.")],
    face_id: Annotated[UUID, Path(description="Face vector ID to delete.")],
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)],
) -> None:
    require_self_or_admin(current_user, user_id)
    await delete_face_vector(face_id, user_id, session)


@router.post(
    "/api/users/{user_id}/faces/from-image",
    response_model=FaceVectorMetadata,
    status_code=status.HTTP_201_CREATED,
    summary="Add a face vector from image",
    description=(
        "Upload an image. The backend detects the largest face, computes a "
        "128-dim SFace embedding, and stores it."
    ),
)
async def add_face_from_image(
    user_id: Annotated[UUID, Path(description="User ID to attach the face to.")],
    image: UploadFile,
    session: SessionDep,
    engine: EngineDep,
    current_user: Annotated[User, Depends(get_current_user)],
    label: Annotated[str | None, Form(min_length=1, max_length=64)] = None,
) -> FaceVectorMetadata:
    require_self_or_admin(current_user, user_id)
    image_bgr = _decode_image(await image.read())
    embedding = engine.detect_and_embed(image_bgr)
    if embedding is None:
        raise NoFaceDetectedError()
    face = await add_face_vector(user_id, embedding, label, session)
    return _to_metadata(face)


@router.post(
    "/api/faces/recognize",
    response_model=RecognizeResponse,
    summary="Recognize a face (stub)",
    description=(
        "Validates the embedding format. Recognition algorithm is not yet implemented."
    ),
)
async def recognize_face(
    request: RecognizeRequest,
    current_user: Annotated[User, Depends(get_current_user)],
) -> RecognizeResponse:
    try:
        request.decode_embedding()
    except ValueError as exc:
        raise InvalidFaceVectorError(detail=str(exc)) from exc

    return RecognizeResponse(
        matched=False,
        user_id=None,
        username=None,
        confidence=0.0,
    )
