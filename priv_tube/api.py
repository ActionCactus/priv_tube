from flask import Flask, Response
import os
import json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
db_file = os.environ["DB_LOCATION"]
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_file}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route("/")
def hello():
    response = Response()
    response.headers.add("Content-Type", "application/json")
    response.set_data(
        json.dumps({"data": {"message": "Big memes", "href": "http://www.google.com"}})
    )
    return response


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
