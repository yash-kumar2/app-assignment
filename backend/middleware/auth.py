from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request


def jwt_required():
    """Simple wrapper around verify_jwt_in_request for central auth middleware."""

    def decorator(fn):
        from functools import wraps

        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def jwt_unauthorized_loader(app):
    """Register a global handler for JWT auth errors."""

    @app.errorhandler(422)
    def handle_unprocessable_entity(err):
        # flask-jwt-extended can raise 422 for some JWT issues
        exc = getattr(err, "exc", None)
        messages = getattr(exc, "messages", ["Invalid request"])
        return jsonify({"message": "Invalid request", "details": messages}), 422

