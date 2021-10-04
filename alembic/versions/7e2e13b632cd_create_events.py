"""Create events

Revision ID: 7e2e13b632cd
Revises: 
Create Date: 2021-10-04 16:42:42.629667

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7e2e13b632cd"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create event status enum (unless exists)
    eventstatus = sa.Enum("published", "draft", "deleted", name="eventstatus")
    eventstatus.create(op.get_bind(), checkfirst=True)

    # Create events
    op.create_table(
        "event",
        sa.Column("created_at", sa.TIMESTAMP(), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("summary", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("starts_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("ends_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("address", sa.String(), nullable=True),
        sa.Column("is_online", sa.Boolean(), nullable=True),
        sa.Column("status_note", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column("event", sa.Column("status", eventstatus, nullable=False))
    op.create_index(op.f("ix_event_ends_at"), "event", ["ends_at"], unique=False)
    op.create_index(op.f("ix_event_starts_at"), "event", ["starts_at"], unique=False)
    op.create_index(op.f("ix_event_url"), "event", ["url"], unique=False)


def downgrade():
    # Drop indices
    op.drop_index(op.f("ix_event_url"), table_name="event")
    op.drop_index(op.f("ix_event_starts_at"), table_name="event")
    op.drop_index(op.f("ix_event_ends_at"), table_name="event")

    # Drop events
    op.drop_table("event")

    # Drop eventstatus enum
    eventstatus = sa.Enum(name="eventstatus")
    eventstatus.drop(op.get_bind(), checkfirst=True)
