"""initial schema

Revision ID: 20240228_000001
Revises: 
Create Date: 2024-02-28 00:00:01.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20240228_000001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    appointment_status = sa.Enum(
        "planned", "confirmed", "done", "canceled", name="appointment_status"
    )
    deal_stage = sa.Enum(
        "new", "consultation", "booked", "done", "upsell", name="deal_stage"
    )
    appointment_status.create(op.get_bind(), checkfirst=True)
    deal_stage.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "tenants",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("timezone", sa.String(), nullable=False),
        sa.Column("plan", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id"), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("full_name", sa.String(), nullable=True),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "clients",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id"), nullable=False),
        sa.Column("full_name", sa.String(), nullable=False),
        sa.Column("phone", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("comment", sa.Text(), nullable=True),
    )

    op.create_table(
        "services",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id"), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("duration_minutes", sa.Integer(), nullable=False),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column("is_medical", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("description", sa.Text(), nullable=True),
    )

    op.create_table(
        "staff",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id"), nullable=False),
        sa.Column("full_name", sa.String(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )

    op.create_table(
        "staff_services",
        sa.Column("staff_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("staff.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("service_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("services.id", ondelete="CASCADE"), primary_key=True),
    )

    op.create_table(
        "appointments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id"), nullable=False),
        sa.Column("client_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("clients.id"), nullable=False),
        sa.Column("staff_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("staff.id"), nullable=False),
        sa.Column("service_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("services.id"), nullable=False),
        sa.Column("start_datetime", sa.DateTime(), nullable=False),
        sa.Column("end_datetime", sa.DateTime(), nullable=False),
        sa.Column("status", appointment_status, nullable=False),
        sa.Column("room", sa.String(), nullable=True),
    )

    op.create_table(
        "deals",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id"), nullable=False),
        sa.Column("client_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("clients.id"), nullable=False),
        sa.Column("stage", deal_stage, nullable=False),
        sa.Column("source", sa.String(), nullable=True),
        sa.Column("ai_summary", sa.Text(), nullable=True),
    )


def downgrade():
    op.drop_table("deals")
    op.drop_table("appointments")
    op.drop_table("staff_services")
    op.drop_table("staff")
    op.drop_table("services")
    op.drop_table("clients")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
    op.drop_table("tenants")
    sa.Enum(name="deal_stage").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="appointment_status").drop(op.get_bind(), checkfirst=True)
