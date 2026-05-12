"""add_mqtt_id_to_door

Revision ID: 3f9c1d2e4b5a
Revises: 2a1a5e3776b6
Create Date: 2026-05-12 17:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlmodel.sql.sqltypes import AutoString

revision: str = "3f9c1d2e4b5a"
down_revision: Union[str, Sequence[str], None] = "2a1a5e3776b6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("door", sa.Column("mqtt_id", AutoString(length=64), nullable=True))
    op.create_index(op.f("ix_door_mqtt_id"), "door", ["mqtt_id"], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_door_mqtt_id"), table_name="door")
    op.drop_column("door", "mqtt_id")
