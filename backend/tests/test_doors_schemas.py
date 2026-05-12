from datetime import datetime, timezone
from uuid import uuid4


def test_door_response_serializes_correctly() -> None:
    from src.doors.schemas import DoorResponse

    door_id = uuid4()
    now = datetime.now(tz=timezone.utc).replace(tzinfo=None)

    resp = DoorResponse(
        id=door_id,
        name="Main Entrance",
        location="Building A",
        is_active=True,
        created_at=now,
    )

    assert resp.id == door_id
    assert resp.name == "Main Entrance"
    assert resp.location == "Building A"
    assert resp.is_active is True


def test_door_list_response_has_pagination_fields() -> None:
    from src.doors.schemas import DoorListResponse, DoorResponse

    now = datetime.now(tz=timezone.utc).replace(tzinfo=None)
    doors = [
        DoorResponse(
            id=uuid4(), name=f"Door {i}", location=None, is_active=True, created_at=now
        )
        for i in range(3)
    ]

    resp = DoorListResponse(total=3, skip=0, limit=10, doors=doors)

    assert resp.total == 3
    assert len(resp.doors) == 3


def test_door_update_request_all_fields_optional() -> None:
    from src.doors.schemas import DoorUpdateRequest

    req = DoorUpdateRequest()

    assert req.name is None
    assert req.location is None
    assert req.is_active is None
