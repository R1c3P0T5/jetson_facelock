from uuid import uuid4

import pytest
from fastapi.routing import APIRoute
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.utils import create_access_token, hash_password
from src.doors.models import Door
from src.users.models import User, UserRole


async def _create_admin_with_token(session: AsyncSession) -> tuple[User, str]:
    admin = User(
        username=f"admin_{uuid4().hex[:10]}",
        email=f"admin_{uuid4().hex[:10]}@example.com",
        password_hash=hash_password("AdminPass123!"),
        full_name="Admin User",
        role=UserRole.ADMIN,
        is_active=True,
    )
    session.add(admin)
    await session.commit()
    await session.refresh(admin)
    return admin, create_access_token(admin.id)


async def _create_door(session: AsyncSession, *, name: str | None = None) -> Door:
    door = Door(name=name or f"door_{uuid4().hex[:12]}")
    session.add(door)
    await session.commit()
    await session.refresh(door)
    return door


def _auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_doors_router_exposes_expected_routes() -> None:
    from src.doors.router import router

    routes = {
        (route.path, tuple(sorted(route.methods or [])))
        for route in router.routes
        if isinstance(route, APIRoute)
    }

    assert router.prefix == "/api/doors"
    assert ("/api/doors", ("GET",)) in routes
    assert ("/api/doors", ("POST",)) in routes
    assert ("/api/doors/{door_id}", ("GET",)) in routes
    assert ("/api/doors/{door_id}", ("PUT",)) in routes
    assert ("/api/doors/{door_id}", ("DELETE",)) in routes


@pytest.mark.asyncio
async def test_list_doors_returns_empty_without_auth(
    client: AsyncClient,
) -> None:
    response = await client.get("/api/doors")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 0
    assert "doors" in data


@pytest.mark.asyncio
async def test_get_door_returns_door_without_auth(
    client: AsyncClient,
    database_session: AsyncSession,
) -> None:
    door = await _create_door(database_session)

    response = await client.get(f"/api/doors/{door.id}")

    assert response.status_code == 200
    assert response.json()["id"] == str(door.id)


@pytest.mark.asyncio
async def test_get_door_returns_404_for_missing_door(
    client: AsyncClient,
) -> None:
    response = await client.get(f"/api/doors/{uuid4()}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Door not found"


@pytest.mark.asyncio
async def test_create_door_requires_admin(
    client: AsyncClient,
) -> None:
    response = await client.post("/api/doors", json={"name": "Locked Out"})

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_door_as_admin_returns_door(
    client: AsyncClient,
    database_session: AsyncSession,
) -> None:
    _, token = await _create_admin_with_token(database_session)

    response = await client.post(
        "/api/doors",
        json={"name": "Server Room", "location": "Floor 3"},
        headers=_auth(token),
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Server Room"
    assert data["location"] == "Floor 3"
    assert data["is_active"] is True
    assert data["id"]


@pytest.mark.asyncio
async def test_create_door_rejects_duplicate_name(
    client: AsyncClient,
    database_session: AsyncSession,
) -> None:
    _, token = await _create_admin_with_token(database_session)
    await _create_door(database_session, name="Unique Door")

    response = await client.post(
        "/api/doors",
        json={"name": "Unique Door"},
        headers=_auth(token),
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Door name already in use"


@pytest.mark.asyncio
async def test_update_door_as_admin_applies_change(
    client: AsyncClient,
    database_session: AsyncSession,
) -> None:
    _, token = await _create_admin_with_token(database_session)
    door = await _create_door(database_session, name="Before Update")

    response = await client.put(
        f"/api/doors/{door.id}",
        json={"is_active": False},
        headers=_auth(token),
    )

    assert response.status_code == 200
    assert response.json()["is_active"] is False


@pytest.mark.asyncio
async def test_update_door_requires_admin(
    client: AsyncClient,
    database_session: AsyncSession,
) -> None:
    door = await _create_door(database_session)

    response = await client.put(f"/api/doors/{door.id}", json={"name": "No Auth"})

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_door_as_admin_returns_204(
    client: AsyncClient,
    database_session: AsyncSession,
) -> None:
    _, token = await _create_admin_with_token(database_session)
    door = await _create_door(database_session)

    response = await client.delete(f"/api/doors/{door.id}", headers=_auth(token))

    assert response.status_code == 204
    assert response.content == b""


@pytest.mark.asyncio
async def test_delete_door_requires_admin(
    client: AsyncClient,
    database_session: AsyncSession,
) -> None:
    door = await _create_door(database_session)

    response = await client.delete(f"/api/doors/{door.id}")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_nonexistent_door_returns_404(
    client: AsyncClient,
    database_session: AsyncSession,
) -> None:
    _, token = await _create_admin_with_token(database_session)

    response = await client.delete(f"/api/doors/{uuid4()}", headers=_auth(token))

    assert response.status_code == 404
