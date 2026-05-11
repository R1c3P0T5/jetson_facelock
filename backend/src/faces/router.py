from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, status

from src.auth.dependencies import get_current_user
from src.core.database import SessionDep
from src.core.exceptions import InvalidFaceVectorError, PermissionDeniedError
from src.faces.models import FaceVector
from src.faces.schemas import (
    FaceVectorCreateRequest,
    FaceVectorListResponse,
    FaceVectorMetadata,
    RecognizeRequest,
    RecognizeResponse,
)
from src.faces.service import add_face_vector, delete_face_vector, list_face_vectors
from src.users.models import User, UserRole


router = APIRouter(tags=["faces"])


def _can_access(current_user: User, user_id: UUID) -> bool:
    return current_user.id == user_id or current_user.role == UserRole.ADMIN


def _ensure_can_access(current_user: User, user_id: UUID) -> None:
    if not _can_access(current_user, user_id):
        raise PermissionDeniedError()


def _to_metadata(face: FaceVector) -> FaceVectorMetadata:
    return FaceVectorMetadata(
        id=face.id,
        label=face.label,
        embedding_size=len(face.embedding),
        created_at=face.created_at,
    )


@router.get(
    "/api/users/{user_id}/faces",
    response_model=FaceVectorListResponse,
    summary="List face vectors",
)
async def list_user_face_vectors(
    user_id: Annotated[UUID, Path(description="User ID whose face vectors to list.")],
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)],
) -> FaceVectorListResponse:
    _ensure_can_access(current_user, user_id)
    faces = await list_face_vectors(user_id, session)
    return FaceVectorListResponse(
        total=len(faces),
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
    _ensure_can_access(current_user, user_id)
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
    _ensure_can_access(current_user, user_id)
    await delete_face_vector(face_id, user_id, session)


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
