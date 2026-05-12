from uuid import uuid4

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.exceptions import (
    DoorMqttIdAlreadyExistsError,
    DoorNameAlreadyExistsError,
    DoorNotFoundError,
)
from src.doors.models import Door
from src.doors.schemas import DoorCreateRequest, DoorUpdateRequest


async def _create_door(
    session: AsyncSession,
    *,
    name: str | None = None,
    mqtt_id: str | None = None,
    location: str | None = None,
    is_active: bool = True,
) -> Door:
    _name = name or f"door_{uuid4().hex[:12]}"
    door = Door(
        name=_name,
        mqtt_id=mqtt_id or _name.lower().replace(" ", "-"),
        location=location,
        is_active=is_active,
    )
    session.add(door)
    await session.commit()
    await session.refresh(door)
    return door


@pytest.mark.asyncio
async def test_get_door_by_id_returns_existing_door(
    database_session: AsyncSession,
) -> None:
    from src.doors.service import get_door_by_id

    door = await _create_door(database_session)

    result = await get_door_by_id(door.id, database_session)

    assert result.id == door.id


@pytest.mark.asyncio
async def test_get_door_by_id_raises_not_found(
    database_session: AsyncSession,
) -> None:
    from src.doors.service import get_door_by_id

    with pytest.raises(DoorNotFoundError):
        await get_door_by_id(uuid4(), database_session)


@pytest.mark.asyncio
async def test_list_doors_returns_total_and_doors(
    database_session: AsyncSession,
) -> None:
    from src.doors.service import list_doors

    created_ids = {(await _create_door(database_session)).id for _ in range(3)}

    total, doors = await list_doors(database_session, skip=0, limit=100)

    assert total >= 3
    assert created_ids.issubset({d.id for d in doors})


@pytest.mark.asyncio
async def test_list_doors_pagination_respects_limit(
    database_session: AsyncSession,
) -> None:
    from src.doors.service import list_doors

    for _ in range(5):
        await _create_door(database_session)

    _, doors = await list_doors(database_session, skip=0, limit=2)

    assert len(doors) <= 2


@pytest.mark.asyncio
async def test_create_door_persists_and_returns_door(
    database_session: AsyncSession,
) -> None:
    from src.doors.service import create_door

    req = DoorCreateRequest(
        name="Front Gate", mqtt_id="front-gate", location="North Wing"
    )

    door = await create_door(req, database_session)

    assert door.name == "Front Gate"
    assert door.mqtt_id == "front-gate"
    assert door.location == "North Wing"
    assert door.is_active is True
    assert door.id is not None


@pytest.mark.asyncio
async def test_create_door_raises_on_duplicate_name(
    database_session: AsyncSession,
) -> None:
    from src.doors.service import create_door

    await _create_door(database_session, name="Duplicate Door", mqtt_id="dup-door")

    with pytest.raises(DoorNameAlreadyExistsError):
        await create_door(
            DoorCreateRequest(name="Duplicate Door", mqtt_id="other-id"),
            database_session,
        )


@pytest.mark.asyncio
async def test_create_door_raises_on_duplicate_mqtt_id(
    database_session: AsyncSession,
) -> None:
    from src.doors.service import create_door

    await _create_door(database_session, name="First Door", mqtt_id="shared-id")

    with pytest.raises(DoorMqttIdAlreadyExistsError):
        await create_door(
            DoorCreateRequest(name="Second Door", mqtt_id="shared-id"),
            database_session,
        )


@pytest.mark.asyncio
async def test_update_door_applies_partial_changes(
    database_session: AsyncSession,
) -> None:
    from src.doors.service import update_door

    door = await _create_door(database_session, name="Old Name", is_active=True)

    result = await update_door(
        door.id, DoorUpdateRequest(is_active=False), database_session
    )

    assert result.id == door.id
    assert result.name == "Old Name"
    assert result.is_active is False


@pytest.mark.asyncio
async def test_update_door_raises_not_found(
    database_session: AsyncSession,
) -> None:
    from src.doors.service import update_door

    with pytest.raises(DoorNotFoundError):
        await update_door(uuid4(), DoorUpdateRequest(name="Ghost"), database_session)


@pytest.mark.asyncio
async def test_update_door_raises_on_duplicate_name(
    database_session: AsyncSession,
) -> None:
    from src.doors.service import update_door

    await _create_door(database_session, name="Taken Name", mqtt_id="taken-name")
    door = await _create_door(
        database_session, name="Original Name", mqtt_id="original-name"
    )

    with pytest.raises(DoorNameAlreadyExistsError):
        await update_door(
            door.id, DoorUpdateRequest(name="Taken Name"), database_session
        )


@pytest.mark.asyncio
async def test_delete_door_removes_it(
    database_session: AsyncSession,
) -> None:
    from src.doors.service import delete_door, get_door_by_id

    door = await _create_door(database_session)

    await delete_door(door.id, database_session)

    with pytest.raises(DoorNotFoundError):
        await get_door_by_id(door.id, database_session)


@pytest.mark.asyncio
async def test_delete_door_raises_not_found(
    database_session: AsyncSession,
) -> None:
    from src.doors.service import delete_door

    with pytest.raises(DoorNotFoundError):
        await delete_door(uuid4(), database_session)
