from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.exceptions import (
    EmailAlreadyInUseError,
    PermissionDeniedError,
    UserNotFoundError,
)
from src.users.models import User, UserRole
from src.users.schemas import MAX_FACE_EMBEDDING_SIZE, UserUpdateRequest


def _now_utc_naive() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _can_modify(user_id: UUID, current_user: User) -> bool:
    return current_user.id == user_id or current_user.role == UserRole.ADMIN


def _ensure_can_modify(user_id: UUID, current_user: User) -> None:
    if not _can_modify(user_id, current_user):
        raise PermissionDeniedError()


async def get_user_by_id(user_id: UUID, session: AsyncSession) -> User:
    user = await session.get(User, user_id)
    if user is None:
        raise UserNotFoundError()
    return user


async def update_user(
    user_id: UUID,
    request: UserUpdateRequest,
    session: AsyncSession,
    current_user: User,
) -> User:
    _ensure_can_modify(user_id, current_user)
    user = await get_user_by_id(user_id, session)

    if request.full_name is not None:
        user.full_name = request.full_name
    if request.email is not None:
        user.email = request.email
    user.updated_at = _now_utc_naive()

    try:
        session.add(user)
        await session.commit()
        await session.refresh(user)
    except IntegrityError as exc:
        await session.rollback()
        if "email" in str(exc).lower():
            raise EmailAlreadyInUseError() from exc
        raise

    return user


async def delete_user(
    user_id: UUID,
    session: AsyncSession,
    current_user: User,
) -> None:
    _ensure_can_modify(user_id, current_user)
    user = await get_user_by_id(user_id, session)

    await session.delete(user)
    await session.commit()


async def update_face_embedding(
    user_id: UUID,
    face_embedding: bytes,
    session: AsyncSession,
    current_user: User,
) -> User:
    _ensure_can_modify(user_id, current_user)
    if len(face_embedding) > MAX_FACE_EMBEDDING_SIZE:
        raise ValueError(
            "Face embedding too large: "
            f"{len(face_embedding)} bytes > {MAX_FACE_EMBEDDING_SIZE} bytes"
        )

    user = await get_user_by_id(user_id, session)
    user.face_embedding = face_embedding
    user.updated_at = _now_utc_naive()

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


async def get_face_embedding(user_id: UUID, session: AsyncSession) -> bytes:
    user = await get_user_by_id(user_id, session)
    if user.face_embedding is None:
        raise UserNotFoundError(detail="Face embedding not found")
    return user.face_embedding


async def list_users(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 10,
) -> tuple[int, list[User]]:
    total = (await session.exec(select(func.count()).select_from(User))).one()
    users = (await session.exec(select(User).offset(skip).limit(limit))).all()

    return total, list(users)
