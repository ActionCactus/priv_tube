"""
Adding initial system settings

Revision ID: caf55027e9a4
Revises: 35b8ff5de06e
Create Date: 2022-03-26 14:14:46.158247

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "caf55027e9a4"
down_revision = "35b8ff5de06e"
branch_labels = None
depends_on = None

settings_table = sa.table(
    "system_flags",
    sa.Column("flag_name", sa.String(length=64), nullable=False),
    sa.Column("value", sa.Boolean(), nullable=False),
)


def upgrade():
    op.bulk_insert(
        settings_table,
        [
            {"flag_name": "system_setup_complete", "value": False},
        ],
    )


def downgrade():
    op.execute("DELETE FROM system_flags WHERE flag_name='system_setup_complete'")
