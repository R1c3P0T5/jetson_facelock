"""add_user_status

Revision ID: 8c3d9e1f2a4b
Revises: 3f9c1d2e4b5a
Create Date: 2026-05-14 00:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "8c3d9e1f2a4b"
down_revision: Union[str, Sequence[str], None] = "3f9c1d2e4b5a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "user",
        sa.Column("status", sa.String(), nullable=False, server_default="approved"),
    )
    op.alter_column("user", "status", server_default=None)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("user", "status")
