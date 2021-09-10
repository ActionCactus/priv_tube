import sys

sys.path.append("./")

from flask import Flask, Response
from werkzeug.serving import run_simple
from priv_tube.cms.content_registry import (
    SQLiteRegistry,
    RegistryNotInitializedException,
)
from traceback import format_exc


app = Flask("priv_tube", template_folder="./priv_tube/web/templates")


def main() -> str:
    retval = "Hello!"
    content_registry = SQLiteRegistry()

    try:
        content_registry.initialize_registry()
        content_registry.check_connection()
    except Exception as e:
        retval = format_exc(e)
    finally:
        content_registry.close_registry_connection()

    return retval


@app.route("/")
def index():
    return Response(main())


if __name__ == "__main__":
    # this is here because we're presently running the app using python, instead of directly using flask
    app.run("localhost", 5000, debug=True)
