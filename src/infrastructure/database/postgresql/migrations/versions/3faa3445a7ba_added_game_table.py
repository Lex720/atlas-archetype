"""Added game table

Revision ID: 3faa3445a7ba
Revises:
Create Date: 2024-05-14 18:11:40.351876

"""

from typing import Sequence

import sqlalchemy as sa
import sqlmodel
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = "3faa3445a7ba"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "games",
        sa.Column("uuid", UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("platform", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("stock", sa.Integer(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("condition", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.PrimaryKeyConstraint("uuid"),
    )
    op.create_index(op.f("ix_games_uuid"), "games", ["uuid"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_games_uuid"), table_name="games")
    op.drop_table("games")
