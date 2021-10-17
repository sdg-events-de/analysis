"""Require suggestion and revision on event

Revision ID: e0dc4f56b9d1
Revises: a9e0824de944
Create Date: 2021-10-17 21:06:19.054791

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e0dc4f56b9d1"
down_revision = "a9e0824de944"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "event", "suggestion_id", existing_type=sa.INTEGER(), nullable=False
    )
    op.alter_column("event", "revision_id", existing_type=sa.INTEGER(), nullable=False)
    op.alter_column(
        "eventversion", "suggestion_id", existing_type=sa.INTEGER(), nullable=False
    )
    op.alter_column(
        "eventversion", "revision_id", existing_type=sa.INTEGER(), nullable=False
    )


def downgrade():
    op.alter_column(
        "eventversion", "revision_id", existing_type=sa.INTEGER(), nullable=True
    )
    op.alter_column(
        "eventversion", "suggestion_id", existing_type=sa.INTEGER(), nullable=True
    )
    op.alter_column("event", "revision_id", existing_type=sa.INTEGER(), nullable=True)
    op.alter_column("event", "suggestion_id", existing_type=sa.INTEGER(), nullable=True)
