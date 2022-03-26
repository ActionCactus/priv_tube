import os
import json
from flask import Flask, Response
from priv_tube.database import db, migrate
from priv_tube.core.boot.initialization_routines.routines import initialize
from priv_tube.core.boot.initialization_routines.execution_targets import ExecutionTargets


app = Flask(__name__)
db_file = os.environ.get("DB_LOCATION")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_file}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.app_context().push()
db.init_app(app)
migrate.init_app(app)

if __name__ == "__main__":
    # Run initialization checks if app is being invoked directly
    initialize(ExecutionTargets.PRE_SYSTEM_CHECK)


@app.route("/")
def hello():
    response = Response()
    response.headers.add("Content-Type", "application/json")

    # List of Row objects: https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Row
    # res = db.session.execute("SELECT * FROM users").all()

    # db_vals = [row._asdict() for row in res]

    response.set_data(
        json.dumps(
            {
                "data": {
                    "message": "Big memes",
                    "db_values": [],  # db_vals,
                    "href": "http://www.google.com",
                }
            },
            indent=4,
        )
    )

    return response


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
