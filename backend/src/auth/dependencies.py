from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.auth.utils import decode_token
from src.core.database import SessionDep
from src.core.exceptions import (
    InactiveUserError,
    InvalidTokenError,
    PermissionDeniedError,
)
from src.users.models import User, UserRole, UserStatus


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep,
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

    user = await session.get(User, user_uuid)

    if user is None:
        raise InvalidTokenError()

    if not user.is_active:
        raise InactiveUserError()

    if user.status != UserStatus.APPROVED:
        raise PermissionDeniedError()

    return user


async def get_admin_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Verify current user has the admin role."""

    if current_user.role != UserRole.ADMIN:
        raise PermissionDeniedError()

    return current_user
