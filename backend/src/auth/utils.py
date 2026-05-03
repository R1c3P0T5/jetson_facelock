from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHash, VerifyMismatchError
from jose import JWTError, jwt

from src.core.exceptions import PasswordValidationError
from src.core.security import (
    COMMON_PASSWORDS,
    JWT_ALGORITHM,
    JWT_EXPIRATION_HOURS,
    MIN_PASSWORD_LENGTH,
    SECRET_KEY,
)


password_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    """Hash password with Argon2id."""

    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against a stored hash."""

    try:
        password_hasher.verify(password_hash, password)
    except (InvalidHash, VerifyMismatchError):
        return False
    return True


def validate_password_strength(
    password: str, username: str, email: str | None = None
) -> None:
    """Validate password strength and raise PasswordValidationError on failure."""

    normalized_password = password.lower()

    if len(password) < MIN_PASSWORD_LENGTH:
        raise PasswordValidationError(
            detail=(f"Password must be at least {MIN_PASSWORD_LENGTH} characters long")
        )

    if normalized_password == username.lower():
        raise PasswordValidationError(detail="Password cannot equal your username")

    if email and normalized_password == email.lower():
        raise PasswordValidationError(detail="Password cannot equal your email")

    if normalized_password in COMMON_PASSWORDS:
        raise PasswordValidationError(
            detail="Password is too common. Please choose a stronger password"
        )


def create_access_token(user_id: UUID) -> str:
    """Create a JWT access token for the given user."""

    expires_at = datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRATION_HOURS)
    payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": expires_at,
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> dict[str, Any] | None:
    """Decode a JWT token, returning None for invalid or expired tokens."""

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except JWTError:
        return None

    if payload.get("sub") is None:
        return None

    return payload
