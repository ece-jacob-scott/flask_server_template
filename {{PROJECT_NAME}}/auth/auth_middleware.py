# Middleware function for authentication

from functools import wraps
from .clerk_client import get_client
from flask import request, make_response, render_template, current_app

def auth_middleware():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            clerk_client = get_client()

            # get the session token from the request cookies
            clerk_session = request.cookies.get("__session", None)

            # if the session token is missing, the user is not authenticated
            if clerk_session is None:
                current_app.logger.error("not authenticated: missing session token")
                response = make_response(render_template("error.html", error="not authenticated"), 401)
                return response

            # verify the session token
            user = clerk_client.verify_session(clerk_session)

            # if the session token is invalid, the user is not authenticated
            if user is None:
                current_app.logger.error("not authenticated: invalid session token")
                response = make_response(render_template("error.html", error="not authenticated"), 401)
                response.set_cookie("__session", "", expires=0)
                return response

            return func(user, *args, **kwargs)
        return wrapper
    return decorator