from fastapi import HTTPException

from src.core.exceptions import (
    BaseAPIError,
    EmailAlreadyInUseError,
    InactiveUserError,
    InvalidCredentialsError,
    InvalidTokenError,
    PasswordValidationError,
    PermissionDeniedError,
    UserNotFoundError,
    UsernameAlreadyExistsError,
)


def test_api_errors_have_expected_default_status_codes_and_details() -> None:
    expected_errors = [
        (UserNotFoundError(), 404, "User not found"),
        (UsernameAlreadyExistsError(), 400, "Username already in use"),
        (EmailAlreadyInUseError(), 400, "Email already in use"),
        (InvalidCredentialsError(), 401, "Invalid username or password"),
        (InactiveUserError(), 403, "User account is disabled"),
        (PermissionDeniedError(), 403, "Permission denied"),
        (
            PasswordValidationError(),
            400,
            "Password does not meet strength requirements",
        ),
        (InvalidTokenError(), 401, "Invalid or expired token"),
    ]

    for error, status_code, detail in expected_errors:
        assert isinstance(error, HTTPException)
        assert error.status_code == status_code
        assert error.detail == detail


def test_base_api_error_can_override_detail_and_status_code() -> None:
    error = BaseAPIError(detail="Custom", status_code=418)

    assert error.status_code == 418
    assert error.detail == "Custom"
