from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col

from src.auth.schemas import UserLoginRequest, UserRegisterRequest
from src.auth.utils import (
    create_access_token,
    hash_password,
    validate_password_strength,
    verify_password,
)
from src.core.exceptions import (
    EmailAlreadyInUseError,
    InactiveUserError,
    InvalidCredentialsError,
    UserNotFoundError,
    UsernameAlreadyExistsError,
)
from src.users.models import User


async def register_user(
    request: UserRegisterRequest,
    session: AsyncSession,
) -> User:
    """Register a new active user."""

    validate_password_strength(request.password, request.username, request.email)
    user = User(
        username=request.username,
        email=request.email,
        password_hash=hash_password(request.password),
        full_name=request.full_name,
        role="user",
        is_active=True,
    )

    try:
        session.add(user)
        await session.commit()
        await session.refresh(user)
    except IntegrityError as exc:
        await session.rollback()
        error = str(exc).lower()
        if "username" in error:
            raise UsernameAlreadyExistsError() from exc
        if "email" in error:
            raise EmailAlreadyInUseError() from exc
        raise

    return user


async def authenticate_user(
    request: UserLoginRequest,
    session: AsyncSession,
) -> tuple[User, str]:
    """Authenticate a user and return the user plus a JWT access token."""

    result = await session.execute(
        select(User).where(col(User.username) == request.username)
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise InvalidCredentialsError()

    if not user.is_active:
        raise InactiveUserError()

    if not verify_password(request.password, user.password_hash):
        raise InvalidCredentialsError()

    return user, create_access_token(user.id)


async def get_user_by_id(user_id: UUID, session: AsyncSession) -> User:
    """Fetch a user by ID."""

    result = await session.execute(select(User).where(col(User.id) == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise UserNotFoundError()

    return user
