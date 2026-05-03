from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col

from src.auth.utils import decode_token
from src.core.database import get_session
from src.core.exceptions import InvalidTokenError, PermissionDeniedError
from src.users.models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> User:
    """Verify JWT access token and return the active current user."""

    payload = decode_token(token)
    if payload is None:
        raise InvalidTokenError()

    user_id = payload.get("sub")
    if not isinstance(user_id, str):
        raise InvalidTokenError()

    try:
        user_uuid = UUID(user_id)
    except ValueError as exc:
        raise InvalidTokenError() from exc

    result = await session.execute(select(User).where(col(User.id) == user_uuid))
    user = result.scalar_one_or_none()

    if user is None or not user.is_active:
        raise InvalidTokenError()

    return user


async def get_admin_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Verify current user has the admin role."""

    if current_user.role != "admin":
        raise PermissionDeniedError()

    return current_user
