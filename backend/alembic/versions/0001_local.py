"""Adopt V0.1 catalog without losing existing identities."""

import sqlalchemy as sa

from alembic import op

revision = "0001"
down_revision = None


def upgrade():
    if "indicators" not in sa.inspect(op.get_bind()).get_table_names():
        op.create_table(
            "indicators",
            sa.Column("id", sa.String(36), primary_key=True),
            sa.Column("code", sa.String(20), nullable=False, unique=True),
            sa.Column("name", sa.String(160), nullable=False),
            sa.Column("definition", sa.Text(), nullable=False),
            sa.Column("domain", sa.String(100)),
            sa.Column("unit", sa.String(60), nullable=False),
            sa.Column("status", sa.String(24), nullable=False),
            sa.Column("created_at", sa.String(40), nullable=False),
            sa.Column("updated_at", sa.String(40), nullable=False),
        )


def downgrade():
    raise RuntimeError("Destructive downgrade disabled; restore a verified backup")
