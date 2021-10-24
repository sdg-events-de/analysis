"""Add logs and log messages

Revision ID: ea4302cc7e18
Revises: e0dc4f56b9d1
Create Date: 2021-10-24 11:41:34.318854

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ea4302cc7e18"
down_revision = "e0dc4f56b9d1"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "log",
        sa.Column("created_at", sa.TIMESTAMP(), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("levelno", sa.Integer(), nullable=True),
        sa.Column("levelname", sa.String(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_log")),
    )
    op.create_table(
        "logmessage",
        sa.Column("created_at", sa.TIMESTAMP(), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("log_id", sa.Integer(), nullable=False),
        sa.Column("logger", sa.String(), nullable=False),
        sa.Column("levelno", sa.Integer(), nullable=False),
        sa.Column("levelname", sa.String(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("trace", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["log_id"], ["log.id"], name=op.f("fk_logmessage_log_id_log")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_logmessage")),
    )
    op.create_index(
        op.f("ix_logmessage_log_id"), "logmessage", ["log_id"], unique=False
    )


def downgrade():
    op.drop_index(op.f("ix_logmessage_log_id"), table_name="logmessage")
    op.drop_table("logmessage")
    op.drop_table("log")
