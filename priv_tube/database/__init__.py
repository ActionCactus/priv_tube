from sqlalchemy.ext.declarative import DeclarativeMeta
from priv_tube.app import db


BaseModel: DeclarativeMeta = db.Model
