from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query, status

from src.auth.dependencies import get_admin_user, get_current_user
from src.auth.schemas import UserResponse
from src.core.database import SessionDep
from src.core.exceptions import InvalidFaceEmbeddingError
from src.users.models import User
from src.users.schemas import (
    UserFaceEmbeddingResponse,
    UserFaceEmbeddingUpdateRequest,
    UserListResponse,
    UserResponseFull,
    UserUpdateRequest,
)
from src.users.service import (
    delete_user,
    get_user_by_id,
    list_users,
    update_face_embedding,
    update_user,
)


router = APIRouter(prefix="/api/users", tags=["users"])


def _face_response(user: User) -> UserFaceEmbeddingResponse:
    return UserFaceEmbeddingResponse(
        id=user.id,
        username=user.username,
        face_embedding_size=len(user.face_embedding or b""),
    )


def _full_user_response(user: User) -> UserResponseFull:
    return UserResponseFull(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
        face_embedding_size=len(user.face_embedding or b""),
    )


@router.get(
    "",
    response_model=UserListResponse,
    summary="List users",
    description=(
        "Return a paginated list of users. This operation is restricted to "
        "administrators because it exposes account metadata for multiple users."
    ),
    response_description="Paginated users with total count and face embedding sizes.",
)
async def list_users_endpoint(
    session: SessionDep,
    current_user: Annotated[User, Depends(get_admin_user)],
    skip: Annotated[
        int,
        Query(
            ge=0,
            description="Number of users to skip before returning results.",
        ),
    ] = 0,
    limit: Annotated[
        int,
        Query(
            ge=1,
            le=100,
            description="Maximum number of users to return.",
        ),
    ] = 10,
) -> UserListResponse:
    total, users = await list_users(session, skip=skip, limit=limit)
    return UserListResponse(
        total=total,
        skip=skip,
        limit=limit,
        users=[_full_user_response(user) for user in users],
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user profile",
    description=(
        "Return a user's public profile by ID. A valid bearer token is required."
    ),
    response_description="The requested user's public profile.",
)
async def get_user(
    user_id: Annotated[UUID, Path(description="User ID to fetch.")],
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    return await get_user_by_id(user_id, session)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user profile",
    description=(
        "Update profile fields for the requested user. Users may update their "
        "own profile; administrators may update any user's profile."
    ),
    response_description="The updated user profile.",
)
async def update_user_profile(
    user_id: Annotated[UUID, Path(description="User ID to update.")],
    request: UserUpdateRequest,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    return await update_user(user_id, request, session, current_user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    description=(
        "Delete the requested user account. Users may delete their own account; "
        "administrators may delete any user account."
    ),
    response_description="No content.",
)
async def delete_user_profile(
    user_id: Annotated[UUID, Path(description="User ID to delete.")],
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)],
) -> None:
    await delete_user(user_id, session, current_user)


@router.put(
    "/{user_id}/face",
    response_model=UserFaceEmbeddingResponse,
    summary="Update face embedding",
    description=(
        "Store a base64-encoded face embedding for a user. Users may update "
        "their own face embedding; administrators may update any user's "
        "embedding. The decoded payload is limited to 2 MiB."
    ),
    response_description="Face embedding metadata after the update.",
)
async def update_user_face(
    user_id: Annotated[UUID, Path(description="User ID whose face embedding changes.")],
    request: UserFaceEmbeddingUpdateRequest,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserFaceEmbeddingResponse:
    try:
        embedding = request.validate_and_decode()
    except ValueError as exc:
        raise InvalidFaceEmbeddingError(detail=str(exc)) from exc

    user = await update_face_embedding(user_id, embedding, session, current_user)
    return _face_response(user)


@router.get(
    "/{user_id}/face",
    response_model=UserFaceEmbeddingResponse,
    summary="Get face embedding metadata",
    description=(
        "Return metadata for a user's stored face embedding. The raw embedding "
        "bytes are not returned through the API."
    ),
    response_description="Face embedding metadata with byte size.",
)
async def get_user_face(
    user_id: Annotated[UUID, Path(description="User ID whose face metadata is read.")],
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserFaceEmbeddingResponse:
    user = await get_user_by_id(user_id, session)
    return _face_response(user)
