from uuid import uuid4

import pytest
from fastapi.routing import APIRoute
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.schemas import LoginResponse, UserRegisterRequest
from src.users.models import User, UserStatus


def test_auth_router_exposes_expected_routes() -> None:
    from src.auth.router import router

    routes = {
        (route.path, tuple(sorted(route.methods or [])))
        for route in router.routes
        if isinstance(route, APIRoute)
    }

    assert router.prefix == "/api/auth"
    assert ("/api/auth/register", ("POST",)) in routes
    assert ("/api/auth/login", ("POST",)) in routes
    assert ("/api/auth/token", ("POST",)) in routes
    assert ("/api/auth/me", ("GET",)) in routes


@pytest.mark.asyncio
async def test_register_endpoint_returns_safe_user_response(
    database_session: AsyncSession,
) -> None:
    from src.auth.router import register

    username = f"router_{uuid4().hex[:12]}"

    response = await register(
        UserRegisterRequest(
            username=username,
            password="MySecurePass123",
            full_name="Router User",
        ),
        database_session,
    )

    assert isinstance(response, User)
    assert response.username == username
    assert response.password_hash != "MySecurePass123"


@pytest.mark.asyncio
async def test_login_endpoint_returns_login_response(
    database_session: AsyncSession,
) -> None:
    from src.auth.router import login, register
    from src.auth.schemas import UserLoginRequest

    username = f"loginrouter_{uuid4().hex[:8]}"
    password = "MySecurePass123"
    user = await register(
        UserRegisterRequest(
            username=username,
            password=password,
            full_name="Login Router",
        ),
        database_session,
    )
    user.status = UserStatus.APPROVED
    database_session.add(user)
    await database_session.commit()

    response = await login(
        UserLoginRequest(username=username, password=password),
        database_session,
    )

    assert isinstance(response, LoginResponse)
    assert response.token_type == "bearer"
    assert response.user.username == username


@pytest.mark.asyncio
async def test_me_endpoint_returns_current_user() -> None:
    from src.auth.router import get_current_user_info

    user = User(
        username="current_user",
        password_hash="hash",
        full_name="Current User",
    )

    response = await get_current_user_info(user)

    assert response is user
    assert response.username == "current_user"
