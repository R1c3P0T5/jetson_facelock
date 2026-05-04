from src.core.config import get_settings
from src.core.security import (
    COMMON_PASSWORDS,
    MIN_PASSWORD_LENGTH,
    get_jwt_algorithm,
    get_jwt_expiration_hours,
    get_secret_key,
)


def test_security_constants_follow_settings_and_password_policy() -> None:
    settings = get_settings()
    assert get_jwt_algorithm() == settings.JWT_ALGORITHM
    assert get_jwt_expiration_hours() == settings.JWT_EXPIRATION_HOURS
    assert get_secret_key() == settings.SECRET_KEY
    assert MIN_PASSWORD_LENGTH == 12
    assert {"password", "123456", "admin"}.issubset(COMMON_PASSWORDS)
