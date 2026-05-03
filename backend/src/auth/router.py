from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user
from src.auth.schemas import (
    LoginResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from src.auth.service import authenticate_user, register_user
from src.core.database import get_session
from src.users.models import User


router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    request: UserRegisterRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> User:
    """Register a new user."""

    return await register_user(request, session)


@router.post("/login", response_model=LoginResponse)
async def login(
    request: UserLoginRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> LoginResponse:
    """Authenticate a user and return an access token."""

    user, token = await authenticate_user(request, session)
    return LoginResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserResponse:
    """Return the current authenticated user."""

    return UserResponse.model_validate(current_user)
