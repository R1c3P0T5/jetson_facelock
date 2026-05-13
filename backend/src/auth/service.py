from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.schemas import UserLoginRequest, UserRegisterRequest
from src.auth.utils import (
    create_access_token,
    hash_password,
    validate_password_strength,
    verify_password,
)
from src.core.config import Settings
from src.core.exceptions import (
    EmailAlreadyInUseError,
    InactiveUserError,
    InvalidCredentialsError,
    PendingApprovalError,
    RejectedApprovalError,
    UsernameAlreadyExistsError,
)
from src.users.models import User, UserRole, UserStatus


async def ensure_default_admin(
    settings: Settings, session: AsyncSession
) -> User | None:
    """Create the configured default admin once, without overwriting existing users."""

    if (
        settings.DEFAULT_ADMIN_USERNAME is None
        or settings.DEFAULT_ADMIN_PASSWORD is None
    ):
        return None

    existing_user = (
        await session.exec(
            select(User).where(User.username == settings.DEFAULT_ADMIN_USERNAME)
        )
    ).one_or_none()
    if existing_user is not None:
        return existing_user

    validate_password_strength(
        settings.DEFAULT_ADMIN_PASSWORD,
        settings.DEFAULT_ADMIN_USERNAME,
        settings.DEFAULT_ADMIN_EMAIL,
    )
    admin = User(
        username=settings.DEFAULT_ADMIN_USERNAME,
        email=settings.DEFAULT_ADMIN_EMAIL,
        password_hash=hash_password(settings.DEFAULT_ADMIN_PASSWORD),
        full_name=settings.DEFAULT_ADMIN_FULL_NAME or settings.DEFAULT_ADMIN_USERNAME,
        role=UserRole.ADMIN,
        status=UserStatus.APPROVED,
        is_active=True,
    )
    session.add(admin)
    await session.commit()
    return admin


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
        role=UserRole.USER,
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
    user = (
        await session.exec(select(User).where(User.username == request.username))
    ).one_or_none()

    if user is None:
        raise InvalidCredentialsError()

    if not verify_password(request.password, user.password_hash):
        raise InvalidCredentialsError()

    if not user.is_active:
        raise InactiveUserError()

    if user.status == UserStatus.PENDING:
        raise PendingApprovalError()

    if user.status == UserStatus.REJECTED:
        raise RejectedApprovalError()

    return user, create_access_token(user.id)
