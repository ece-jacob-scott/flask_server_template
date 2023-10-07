from flask import Flask, g, current_app


def get_db() -> database_manager.DatabaseManager:
    # if "db" not in g:
    #     g.db = database_manager.DatabaseManager(
    #         current_app.config["DB_HOST"],
    #         current_app.config["DB_USER"],
    #         current_app.config["DB_PASSWORD"],
    #         current_app.config["DB_NAME"],
    #     )

    return g.db


def teardown_db(ex):
    return
    # db_manager = g.pop("db_manager", None)

    # if db is not None:
    #     db._close()
    #     app.logger.info("database connection closed")
    # else:
    #     app.logger.info("database connection not found")


def init_app(app: Flask):
    app.teardown_appcontext(teardown_db)
