from flask import Flask, render_template
from werkzeug.serving import run_simple

app = Flask("priv_tube", template_folder="./priv_tube/web/templates")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    # this is here because we're presently running the app using python, instead of directly using flask
    run_simple("localhost", 5000, app)