from priv_tube.database import BaseModel, db


class User(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=True)
