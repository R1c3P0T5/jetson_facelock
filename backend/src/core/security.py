from src.core.config import get_settings


def get_jwt_algorithm() -> str:
    return get_settings().JWT_ALGORITHM


def get_jwt_expiration_hours() -> int:
    return get_settings().JWT_EXPIRATION_HOURS


def get_secret_key() -> str:
    return get_settings().SECRET_KEY


MIN_PASSWORD_LENGTH = 12
COMMON_PASSWORDS = {
    "password",
    "123456",
    "12345678",
    "qwerty",
    "abc123",
    "password123",
    "admin",
    "letmein",
    "welcome",
    "monkey",
}
