"""Create event versions

Revision ID: dbe870a8f987
Revises: 7e2e13b632cd
Create Date: 2021-10-04 16:56:09.526544

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "dbe870a8f987"
down_revision = "7e2e13b632cd"
branch_labels = None
depends_on = None


def upgrade():
    # Create event status enum (unless exists)
    eventstatus = sa.Enum("published", "draft", "deleted", name="eventstatus")
    eventstatus.create(op.get_bind(), checkfirst=True)

    # Create version action enum (unless exists)
    versionaction = sa.Enum(
        "create", "discover", "edit", "review", "suggest", name="versionaction"
    )
    versionaction.create(op.get_bind(), checkfirst=True)

    # Create event versions
    op.create_table(
        "eventversion",
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
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("hash_id", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["event_id"],
            ["event.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column("eventversion", sa.Column("status", eventstatus, nullable=False))
    op.add_column("eventversion", sa.Column("action", versionaction, nullable=False))

    op.create_index(
        op.f("ix_eventversion_ends_at"), "eventversion", ["ends_at"], unique=False
    )
    op.create_index(
        op.f("ix_eventversion_event_id"), "eventversion", ["event_id"], unique=False
    )
    op.create_index(
        op.f("ix_eventversion_starts_at"), "eventversion", ["starts_at"], unique=False
    )
    op.create_index(op.f("ix_eventversion_url"), "eventversion", ["url"], unique=False)


def downgrade():
    # Drop indices
    op.drop_index(op.f("ix_eventversion_url"), table_name="eventversion")
    op.drop_index(op.f("ix_eventversion_starts_at"), table_name="eventversion")
    op.drop_index(op.f("ix_eventversion_event_id"), table_name="eventversion")
    op.drop_index(op.f("ix_eventversion_ends_at"), table_name="eventversion")

    # Drop table
    op.drop_table("eventversion")

    # Drop versionaction enum
    versionaction = sa.Enum(name="versionaction")
    versionaction.drop(op.get_bind(), checkfirst=True)
