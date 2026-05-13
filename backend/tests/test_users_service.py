from uuid import UUID, uuid4

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.exceptions import (
    EmailAlreadyInUseError,
    PermissionDeniedError,
    UserNotFoundError,
)
from src.users.models import User, UserRole, UserStatus
from src.users.schemas import UserUpdateRequest


async def create_user(
    session: AsyncSession,
    *,
    username: str | None = None,
    email: str | None = None,
    role: UserRole = UserRole.USER,
    status: UserStatus = UserStatus.APPROVED,
) -> User:
    user = User(
        username=username or f"user_{uuid4().hex[:12]}",
        email=email,
        password_hash="hash",
        full_name="Original Name",
        role=role,
        status=status,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@pytest.mark.asyncio
async def test_get_user_by_id_returns_existing_user(
    database_session: AsyncSession,
) -> None:
    from src.users.service import get_user_by_id

    user = await create_user(database_session)

    result = await get_user_by_id(user.id, database_session)

    assert result.id == user.id


@pytest.mark.asyncio
async def test_update_user_allows_self_and_updates_timestamp(
    database_session: AsyncSession,
) -> None:
    from src.users.service import update_user

    user = await create_user(database_session)
    original_updated_at = user.updated_at

    result = await update_user(
        user.id,
        UserUpdateRequest(full_name="Updated Name"),
        database_session,
        user,
    )

    assert result.full_name == "Updated Name"
    assert result.updated_at > original_updated_at


@pytest.mark.asyncio
async def test_update_user_allows_admin_to_update_another_user(
    database_session: AsyncSession,
) -> None:
    from src.users.service import update_user

    admin = await create_user(database_session, role=UserRole.ADMIN)
    user = await create_user(database_session)

    result = await update_user(
        user.id,
        UserUpdateRequest(
            full_name=None,
            email=f"{uuid4().hex[:12]}@example.com",
        ),
        database_session,
        admin,
    )

    assert result.id == user.id
    assert result.email is not None


@pytest.mark.asyncio
async def test_update_user_rejects_non_owner(
    database_session: AsyncSession,
) -> None:
    from src.users.service import update_user

    current_user = await create_user(database_session)
    target_user = await create_user(database_session)

    with pytest.raises(PermissionDeniedError):
        await update_user(
            target_user.id,
            UserUpdateRequest(full_name="Nope"),
            database_session,
            current_user,
        )


@pytest.mark.asyncio
async def test_update_user_rejects_duplicate_email(
    database_session: AsyncSession,
) -> None:
    from src.users.service import update_user

    email = f"{uuid4().hex[:12]}@example.com"
    await create_user(database_session, email=email)
    user = await create_user(database_session)

    with pytest.raises(EmailAlreadyInUseError):
        await update_user(
            user.id,
            UserUpdateRequest(full_name=None, email=email),
            database_session,
            user,
        )


@pytest.mark.asyncio
async def test_delete_user_allows_admin_to_delete_user(
    database_session: AsyncSession,
) -> None:
    from src.users.service import delete_user, get_user_by_id

    admin = await create_user(database_session, role=UserRole.ADMIN)
    user = await create_user(database_session)

    assert await delete_user(user.id, database_session, admin) is None

    with pytest.raises(UserNotFoundError):
        await get_user_by_id(user.id, database_session)


@pytest.mark.asyncio
async def test_list_users_returns_total_and_paginated_users(
    database_session: AsyncSession,
) -> None:
    from src.users.service import list_users

    created_ids: set[UUID] = set()
    for _ in range(3):
        user = await create_user(database_session)
        created_ids.add(user.id)

    total, users = await list_users(database_session, skip=0, limit=100)

    assert total >= 3
    assert created_ids.issubset({user.id for user in users})


@pytest.mark.asyncio
async def test_list_users_filters_by_status(
    database_session: AsyncSession,
) -> None:
    from src.users.service import list_users

    pending_user = await create_user(database_session, status=UserStatus.PENDING)
    await create_user(database_session, status=UserStatus.APPROVED)

    total, users = await list_users(
        database_session, skip=0, limit=100, status=UserStatus.PENDING
    )

    assert total == 1
    assert users[0].id == pending_user.id


@pytest.mark.asyncio
async def test_approve_user_sets_status_and_updates_timestamp(
    database_session: AsyncSession,
) -> None:
    from src.users.service import approve_user

    user = await create_user(database_session, status=UserStatus.PENDING)
    original_updated_at = user.updated_at

    result = await approve_user(user.id, database_session)

    assert result.status == UserStatus.APPROVED
    assert result.updated_at > original_updated_at


@pytest.mark.asyncio
async def test_approve_user_allows_rejected_user_recovery(
    database_session: AsyncSession,
) -> None:
    from src.users.service import approve_user

    user = await create_user(database_session, status=UserStatus.REJECTED)

    result = await approve_user(user.id, database_session)

    assert result.status == UserStatus.APPROVED


@pytest.mark.asyncio
async def test_reject_user_sets_status_and_updates_timestamp(
    database_session: AsyncSession,
) -> None:
    from src.users.service import reject_user

    user = await create_user(database_session, status=UserStatus.PENDING)
    original_updated_at = user.updated_at

    result = await reject_user(user.id, database_session)

    assert result.status == UserStatus.REJECTED
    assert result.updated_at > original_updated_at


@pytest.mark.asyncio
async def test_approve_user_rejects_missing_user(
    database_session: AsyncSession,
) -> None:
    from src.users.service import approve_user

    with pytest.raises(UserNotFoundError):
        await approve_user(uuid4(), database_session)


@pytest.mark.asyncio
async def test_reject_user_rejects_missing_user(
    database_session: AsyncSession,
) -> None:
    from src.users.service import reject_user

    with pytest.raises(UserNotFoundError):
        await reject_user(uuid4(), database_session)
