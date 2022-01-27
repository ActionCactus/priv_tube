"""Initial user seed

Revision ID: 35b8ff5de06e
Revises: 11cc9f9909c6
Create Date: 2022-01-27 01:44:16.436195

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

# revision identifiers, used by Alembic.
revision = "35b8ff5de06e"
down_revision = "11cc9f9909c6"
branch_labels = None
depends_on = None


def upgrade():
    usr_tbl = table(
        "users",
        column("id", sa.Integer()),
        column("first_name", sa.String(length=128)),
        column("last_name", sa.String(length=128)),
    )
    op.bulk_insert(usr_tbl, [{"first_name": "First Name", "last_name": "Last Name"}])


def downgrade():
    pass
