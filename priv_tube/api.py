from flask import Flask, Response
import os
import json

app = Flask(__name__)


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
