from priv_tube.database import BaseModel, db


class SystemFlags(BaseModel):
    flag_name = db.Column(db.String(64), primary_key=True)
    value = db.Column(db.Boolean, default=False, nullable=False)
