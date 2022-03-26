"""Initial user seed

Revision ID: 35b8ff5de06e
Revises: 11cc9f9909c6
Create Date: 2022-01-27 01:44:16.436195

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table

# revision identifiers, used by Alembic.
revision = "35b8ff5de06e"
down_revision = "19c438dc3eb8"
branch_labels = None
depends_on = None


def upgrade():
    usr_tbl = table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("display_name", sa.String(length=128), nullable=False),
        sa.Column("first_name", sa.String(length=128), nullable=False),
        sa.Column("last_name", sa.String(length=128), nullable=False),
        sa.Column("email", sa.String(length=128), nullable=True),
    )
    op.bulk_insert(usr_tbl, [{"display_name": "Test User", "first_name": "First Name", "last_name": "Last Name"}])


def downgrade():
    # Truncate the entire table
    op.execute("DELETE FROM user WHERE first_name='First Name' AND last_name='Last Name' AND display_name='Test User';")
