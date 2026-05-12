from uuid import UUID

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.exceptions import DoorNameAlreadyExistsError, DoorNotFoundError
from src.doors.models import Door
from src.doors.schemas import DoorCreateRequest, DoorUpdateRequest


async def get_door_by_id(door_id: UUID, session: AsyncSession) -> Door:
    door = await session.get(Door, door_id)
    if door is None:
        raise DoorNotFoundError()
    return door


async def list_doors(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 10,
) -> tuple[int, list[Door]]:
    total = (await session.exec(select(func.count()).select_from(Door))).one()
    doors = list((await session.exec(select(Door).offset(skip).limit(limit))).all())
    return total, doors


async def create_door(request: DoorCreateRequest, session: AsyncSession) -> Door:
    door = Door(
        name=request.name,
        location=request.location,
        is_active=request.is_active,
    )
    session.add(door)
    try:
        await session.commit()
        await session.refresh(door)
    except IntegrityError as exc:
        await session.rollback()
        raise DoorNameAlreadyExistsError() from exc
    return door


async def update_door(
    door_id: UUID,
    request: DoorUpdateRequest,
    session: AsyncSession,
) -> Door:
    door = await get_door_by_id(door_id, session)

    if request.name is not None:
        door.name = request.name
    if request.location is not None:
        door.location = request.location
    if request.is_active is not None:
        door.is_active = request.is_active

    session.add(door)
    try:
        await session.commit()
        await session.refresh(door)
    except IntegrityError as exc:
        await session.rollback()
        raise DoorNameAlreadyExistsError() from exc
    return door


async def delete_door(door_id: UUID, session: AsyncSession) -> None:
    door = await get_door_by_id(door_id, session)
    await session.delete(door)
    await session.commit()
