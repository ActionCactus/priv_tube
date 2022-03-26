"""
App bootstrap for running Flask-Migrate commands.
"""

from priv_tube.database import db
from priv_tube.app import app, migrate
from priv_tube.database.models import *
