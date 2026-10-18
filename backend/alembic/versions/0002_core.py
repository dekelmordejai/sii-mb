"""Core entities, access control and immutable analytical history."""
from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"


def ident():
    return sa.Column("id", sa.String(36), primary_key=True)


def timestamp():
    return sa.Column("created_at", sa.String(40), nullable=False)


def upgrade():
    op.add_column("indicators", sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()))
    op.add_column("indicators", sa.Column("dimensions_json", sa.Text(), nullable=False, server_default="[]"))
    op.create_table("users", ident(), sa.Column("username", sa.String(80), nullable=False, unique=True),
        sa.Column("password_hash", sa.Text(), nullable=False), sa.Column("role", sa.String(20), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False), sa.Column("scopes_json", sa.Text(), nullable=False), timestamp())
    op.create_table("login_sessions", sa.Column("token_hash", sa.String(64), primary_key=True),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id"), nullable=False), sa.Column("expires_at", sa.Float(), nullable=False))
    op.create_table("login_attempts", sa.Column("key", sa.String(64), primary_key=True),
        sa.Column("failures", sa.Integer(), nullable=False), sa.Column("blocked_until", sa.Float(), nullable=False))
    op.create_table("audit_events", ident(), sa.Column("actor_id", sa.String(36), nullable=False),
        sa.Column("action", sa.String(80), nullable=False), sa.Column("object_id", sa.String(80), nullable=False),
        sa.Column("detail_json", sa.Text(), nullable=False), timestamp())
    op.create_table("sources", ident(), sa.Column("name", sa.String(160), nullable=False), sa.Column("kind", sa.String(20), nullable=False),
        sa.Column("sha256", sa.String(64), nullable=False), sa.Column("content", sa.Text(), nullable=False),
        sa.Column("profile_json", sa.Text(), nullable=False), timestamp())
    op.create_table("methods", ident(), sa.Column("indicator_id", sa.String(36), sa.ForeignKey("indicators.id"), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False), sa.Column("config_json", sa.Text(), nullable=False), timestamp(),
        sa.UniqueConstraint("indicator_id", "version"))
    op.create_table("runs", ident(), sa.Column("method_id", sa.String(36), sa.ForeignKey("methods.id"), nullable=False),
        sa.Column("source_id", sa.String(36), sa.ForeignKey("sources.id"), nullable=False), sa.Column("request_json", sa.Text(), nullable=False),
        sa.Column("result_json", sa.Text(), nullable=False), sa.Column("engine_version", sa.String(30), nullable=False), timestamp())
    op.create_table("indicator_relations", ident(), sa.Column("source_id", sa.String(36), sa.ForeignKey("indicators.id"), nullable=False),
        sa.Column("target_id", sa.String(36), sa.ForeignKey("indicators.id"), nullable=False), sa.Column("label", sa.String(100), nullable=False),
        sa.UniqueConstraint("source_id", "target_id", "label"))
    op.create_table("dashboards", ident(), sa.Column("owner_id", sa.String(36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("name", sa.String(160), nullable=False), sa.Column("config_json", sa.Text(), nullable=False), timestamp())


def downgrade():
    raise RuntimeError("Destructive downgrade disabled; restore a verified backup")
