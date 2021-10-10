"""Remove hash_id from event versions

Revision ID: 7b6c247ac499
Revises: dbe870a8f987
Create Date: 2021-10-10 17:56:45.460412

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7b6c247ac499"
down_revision = "dbe870a8f987"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("eventversion", "hash_id")


def downgrade():
    op.add_column("eventversion", sa.Column("hash_id", sa.String(), nullable=False))
