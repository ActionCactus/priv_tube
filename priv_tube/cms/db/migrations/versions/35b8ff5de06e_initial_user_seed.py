"""Initial user seed

Revision ID: 35b8ff5de06e
Revises: 11cc9f9909c6
Create Date: 2022-01-27 01:44:16.436195

"""
from alembic import op
import sqlalchemy as sa
import sqlite3


# revision identifiers, used by Alembic.
revision = "35b8ff5de06e"
down_revision = "11cc9f9909c6"
branch_labels = None
depends_on = None


def upgrade():
    connection = sqlite3.connect("app.db")
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO users(first_name, last_name) VALUES ("First Name", "Last Name");
        """
    )

    inserted_data = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(inserted_data.fetchall())


def downgrade():
    pass
