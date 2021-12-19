"""Create user table

Revision ID: a824bcdd1067
Revises:
Create Date: 2021-03-17 22:15:36.845375

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a824bcdd1067"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("first_name", sa.VARCHAR(255), primary_key=True),
        sa.Column("last_name", sa.VARCHAR(255), primary_key=True),
    )


def downgrade():
    pass
