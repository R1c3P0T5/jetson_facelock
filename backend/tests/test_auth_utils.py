from uuid import uuid4

import pytest

from src.core.exceptions import PasswordValidationError


def test_password_hashing_verifies_original_password() -> None:
    from src.auth.utils import hash_password, verify_password

    password = "MySecurePass123"

    password_hash = hash_password(password)

    assert password_hash
    assert password_hash != password
    assert verify_password(password, password_hash) is True
    assert verify_password("WrongPassword123", password_hash) is False


@pytest.mark.parametrize(
    ("password", "username", "email", "message"),
    [
        ("short", "john_doe", None, "at least 12 characters"),
        ("john_doe_1234", "john_doe_1234", None, "username"),
        ("john@example.com", "john_doe", "john@example.com", "email"),
        ("password123", "john_doe", None, "at least 12 characters"),
    ],
)
def test_password_strength_rejects_weak_passwords(
    password: str, username: str, email: str | None, message: str
) -> None:
    from src.auth.utils import validate_password_strength

    with pytest.raises(PasswordValidationError, match=message):
        validate_password_strength(password, username, email)


def test_password_strength_accepts_strong_password() -> None:
    from src.auth.utils import validate_password_strength

    assert (
        validate_password_strength("MySecurePass123", "john_doe", "john@example.com")
        is None
    )


def test_access_token_round_trips_user_id_and_type() -> None:
    from src.auth.utils import create_access_token, decode_token

    user_id = uuid4()

    token = create_access_token(user_id)
    payload = decode_token(token)

    assert payload is not None
    assert payload["sub"] == str(user_id)
    assert payload["type"] == "access"
    assert "exp" in payload


def test_decode_token_returns_none_for_invalid_token() -> None:
    from src.auth.utils import decode_token

    assert decode_token("invalid.token.here") is None
