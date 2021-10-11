"""Add suggestion and revision to events

Revision ID: e359e36e10ce
Revises: 7b6c247ac499
Create Date: 2021-10-10 19:20:15.657401

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e359e36e10ce"
down_revision = "7b6c247ac499"
branch_labels = None
depends_on = None


def upgrade():
    # Re-use event status enum
    eventstatus = sa.Enum(name="eventstatus")

    op.create_table(
        "eventsuggestion",
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
        sa.PrimaryKeyConstraint("id", name=op.f("pk_eventsuggestion")),
    )
    op.add_column("eventsuggestion", sa.Column("status", eventstatus, nullable=False))

    op.create_index(
        op.f("ix_eventsuggestion_ends_at"), "eventsuggestion", ["ends_at"], unique=False
    )
    op.create_index(
        op.f("ix_eventsuggestion_starts_at"),
        "eventsuggestion",
        ["starts_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_eventsuggestion_url"), "eventsuggestion", ["url"], unique=False
    )
    op.add_column("event", sa.Column("suggestion_id", sa.Integer(), nullable=True))
    op.add_column("event", sa.Column("revision_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        op.f("fk_event_suggestion_id_eventsuggestion"),
        "event",
        "eventsuggestion",
        ["suggestion_id"],
        ["id"],
    )
    op.create_foreign_key(
        op.f("fk_event_revision_id_eventsuggestion"),
        "event",
        "eventsuggestion",
        ["revision_id"],
        ["id"],
    )
    op.add_column(
        "eventversion", sa.Column("suggestion_id", sa.Integer(), nullable=True)
    )
    op.add_column("eventversion", sa.Column("revision_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        op.f("fk_eventversion_revision_id_eventsuggestion"),
        "eventversion",
        "eventsuggestion",
        ["revision_id"],
        ["id"],
    )
    op.create_foreign_key(
        op.f("fk_eventversion_suggestion_id_eventsuggestion"),
        "eventversion",
        "eventsuggestion",
        ["suggestion_id"],
        ["id"],
    )


def downgrade():
    op.drop_constraint(
        op.f("fk_eventversion_suggestion_id_eventsuggestion"),
        "eventversion",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f("fk_eventversion_revision_id_eventsuggestion"),
        "eventversion",
        type_="foreignkey",
    )
    op.drop_column("eventversion", "revision_id")
    op.drop_column("eventversion", "suggestion_id")
    op.drop_constraint(
        op.f("fk_event_revision_id_eventsuggestion"), "event", type_="foreignkey"
    )
    op.drop_constraint(
        op.f("fk_event_suggestion_id_eventsuggestion"), "event", type_="foreignkey"
    )
    op.drop_column("event", "revision_id")
    op.drop_column("event", "suggestion_id")
    op.drop_index(op.f("ix_eventsuggestion_url"), table_name="eventsuggestion")
    op.drop_index(op.f("ix_eventsuggestion_starts_at"), table_name="eventsuggestion")
    op.drop_index(op.f("ix_eventsuggestion_ends_at"), table_name="eventsuggestion")
    op.drop_table("eventsuggestion")
