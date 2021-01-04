from flask import Flask, render_template
from werkzeug.serving import run_simple

app = Flask("priv_tube")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    run_simple("localhost", 5000, app)