from fastapi import HTTPException

from src.core.exceptions import (
    BaseAPIError,
    EmailAlreadyInUseError,
    InactiveUserError,
    InvalidCredentialsError,
    InvalidTokenError,
    PasswordValidationError,
    PendingApprovalError,
    PermissionDeniedError,
    RejectedApprovalError,
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
        (PendingApprovalError(), 403, "approval_pending"),
        (
            RejectedApprovalError(),
            403,
            "User account approval was rejected",
        ),
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


def test_door_not_found_error_has_correct_status_and_detail() -> None:
    from src.core.exceptions import DoorNotFoundError

    err = DoorNotFoundError()

    assert err.status_code == 404
    assert err.detail == "Door not found"


def test_door_name_already_exists_error_has_correct_status_and_detail() -> None:
    from src.core.exceptions import DoorNameAlreadyExistsError

    err = DoorNameAlreadyExistsError()

    assert err.status_code == 400
    assert err.detail == "Door name already in use"
