from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

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


@router.get("", response_model=UserListResponse)
async def list_users_endpoint(
    session: SessionDep,
    current_user: Annotated[User, Depends(get_admin_user)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
) -> UserListResponse:
    """List all users. Admin only."""

    total, users = await list_users(session, skip=skip, limit=limit)
    return UserListResponse(
        total=total,
        skip=skip,
        limit=limit,
        users=[_full_user_response(user) for user in users],
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Get user profile."""

    return await get_user_by_id(user_id, session)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user_profile(
    user_id: UUID,
    request: UserUpdateRequest,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Update user profile."""

    return await update_user(user_id, request, session, current_user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_profile(
    user_id: UUID,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)],
) -> None:
    """Delete user profile."""

    await delete_user(user_id, session, current_user)


@router.put("/{user_id}/face", response_model=UserFaceEmbeddingResponse)
async def update_user_face(
    user_id: UUID,
    request: UserFaceEmbeddingUpdateRequest,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserFaceEmbeddingResponse:
    """Update user face embedding."""

    try:
        embedding = request.validate_and_decode()
    except ValueError as exc:
        raise InvalidFaceEmbeddingError(detail=str(exc)) from exc

    user = await update_face_embedding(user_id, embedding, session, current_user)
    return _face_response(user)


@router.get("/{user_id}/face", response_model=UserFaceEmbeddingResponse)
async def get_user_face(
    user_id: UUID,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserFaceEmbeddingResponse:
    """Get face embedding metadata."""

    user = await get_user_by_id(user_id, session)
    return _face_response(user)
