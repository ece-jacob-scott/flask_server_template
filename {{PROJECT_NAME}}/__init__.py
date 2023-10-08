from os import environ
from flask import (
    Flask,
    render_template,
    request,
    current_app,
    Response,
)
import logging
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from . import logger
from . import auth

db = SQLAlchemy()


# TODO: maybe this is just worse than a config file?
def load_config(app: Flask):
    config_vars = [
        "FLASK_APP",
        "HAS_AUTH",
        "HAS_DATABASE",
        "APP_VERSION",
        "FLASK_ENV",
    ]

    if environ.get("HAS_AUTH") is not None and environ["HAS_AUTH"] == "true":
        config_vars.extend(
            [
                "CLERK_FRONTEND_KEY",
                "CLERK_BACKEND_KEY",
            ]
        )

    # TODO: this is a bit of a hack, but it works for now
    if environ.get("HAS_DATABASE") is not None and environ["HAS_DATABASE"] == "true":
        config_vars.extend(
            ["SQLALCHEMY_DATABASE_URI", "SQLALCHEMY_TRACK_MODIFICATIONS"]
        )

    for var in config_vars:
        if environ.get(var) is None:
            raise Exception(f"{var} must be provided")
        app.config[var] = environ[var]


def create_app():
    # setup logging
    logger.setup_logging()

    app = Flask(__name__)
    load_config(app)

    # setup FLASK_ENV defaults
    if app.config["FLASK_ENV"] == "development":
        app.config["DEBUG"] = True
        app.config["TEMPLATES_AUTO_RELOAD"] = True
        app.logger.setLevel(logging.DEBUG)
    else:
        app.logger.setLevel(logging.INFO)

    # setup database
    if app.config["HAS_DATABASE"]:
        db.init_app(app)
        from .models import users_table

    @app.before_request
    def log_before_request():
        # add a unique id to the request
        request.id = str(uuid4())
        current_app.logger.info(f"request [{request.method} {request.full_path}]")

    @app.after_request
    def log_after_request(response: Response):
        current_app.logger.info(
            f"response [{request.method} {request.full_path} {response.status_code}]"
        )
        return response

    @app.route("/")
    def hello_world():
        app.logger.info("hello world")
        return render_template("index.html", name="World!")

    @app.route("/error")
    def trigger_error():
        return render_template("error.html", error="you triggered an error"), 500

    @app.route("/protected")
    @auth.auth_middleware()
    def protected(user: auth.ClerkUser):
        if current_app.config["HAS_DATABASE"]:
            current_app.logger.info(f"insert: {users_table.insert()}")
        return user.id

    @app.route("/health", methods=["GET"])
    def health():
        return "OK"

    @app.cli.command("create_database")
    def create_database():
        if app.config["HAS_DATABASE"]:
            db.create_all()

    return app
