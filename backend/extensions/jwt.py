from flask_jwt_extended import JWTManager

jwt = JWTManager()


def init_jwt(app):
    """Initialize JWT manager with the Flask app."""
    jwt.init_app(app)

