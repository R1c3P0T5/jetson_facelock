from src.core.config import settings
from src.core.security import (
    COMMON_PASSWORDS,
    JWT_ALGORITHM,
    JWT_EXPIRATION_HOURS,
    MIN_PASSWORD_LENGTH,
    SECRET_KEY,
)


def test_security_constants_follow_settings_and_password_policy() -> None:
    assert JWT_ALGORITHM == settings.JWT_ALGORITHM
    assert JWT_EXPIRATION_HOURS == settings.JWT_EXPIRATION_HOURS
    assert SECRET_KEY == settings.SECRET_KEY
    assert MIN_PASSWORD_LENGTH == 12
    assert {"password", "123456", "admin"}.issubset(COMMON_PASSWORDS)
