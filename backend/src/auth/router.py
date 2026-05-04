from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.dependencies import get_current_user
from src.auth.schemas import (
    LoginResponse,
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from src.auth.service import authenticate_user, register_user
from src.core.database import SessionDep
from src.users.models import User


router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    request: UserRegisterRequest,
    session: SessionDep,
) -> User:
    """Register a new user account."""

    return await register_user(request, session)


@router.post("/login", response_model=LoginResponse)
async def login(
    request: UserLoginRequest,
    session: SessionDep,
) -> LoginResponse:
    """Authenticate with username/password and receive a JWT access token."""

    user, token = await authenticate_user(request, session)
    return LoginResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
    )


@router.post("/token", response_model=TokenResponse)
async def token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
) -> TokenResponse:
    """OAuth2 Password Flow token endpoint (form-encoded)."""

    user, token_value = await authenticate_user(
        UserLoginRequest(username=form_data.username, password=form_data.password),
        session,
    )
    return TokenResponse(access_token=token_value, token_type="bearer")


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Return the profile of the currently authenticated user."""

    return current_user
