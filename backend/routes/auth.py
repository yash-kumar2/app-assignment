from datetime import timedelta

from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_jwt_identity,
    jwt_required,
)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from models.user import User

auth_bp = Blueprint("auth", __name__)

# Global limiter; will attach to the app without extra kwargs.
limiter = Limiter(key_func=get_remote_address, default_limits=[])


@auth_bp.record_once
def on_load(state):
    """Hook blueprint into the Flask app and bind the limiter."""

    app = state.app
    # For the installed Flask-Limiter version, we just call init_app(app).
    # Storage backend can be configured via app.config if needed.
    limiter.init_app(app)


@auth_bp.post("/signup")
def signup():
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not all([name, email, password]):
        return jsonify({"message": "name, email and password are required"}), 400

    if User.find_by_email(email):
        return jsonify({"message": "Email already registered"}), 400

    User.create(name=name, email=email, password=password)
    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.post("/login")
@limiter.limit(lambda: current_app.config.get("LOGIN_RATE_LIMIT", "5 per minute"))
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not all([email, password]):
        return jsonify({"message": "email and password are required"}), 400

    user = User.find_by_email(email)
    if not user or not user.verify_password(password):
        return jsonify({"message": "Invalid credentials"}), 401

    identity = str(user.data["_id"])
    access_expires: timedelta = current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]
    refresh_expires: timedelta = current_app.config["JWT_REFRESH_TOKEN_EXPIRES"]

    access_token = create_access_token(identity=identity, expires_delta=access_expires)
    refresh_token = create_refresh_token(
        identity=identity, expires_delta=refresh_expires
    )

    return (
        jsonify(
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_in": int(access_expires.total_seconds()),
            }
        ),
        200,
    )


@auth_bp.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.find_by_id(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user.to_public_dict())


@auth_bp.post("/refresh")
def refresh():
    """Issue a new access token from a refresh token in the request body."""
    data = request.get_json() or {}
    refresh_token = data.get("refresh_token")
    if not refresh_token:
        return jsonify({"message": "refresh_token is required"}), 400

    try:
        decoded = decode_token(refresh_token)
    except Exception:
        return jsonify({"message": "Invalid refresh token"}), 401

    if decoded.get("type") != "refresh":
        return jsonify({"message": "Invalid token type"}), 401

    user_id = decoded.get("sub")
    if not user_id:
        return jsonify({"message": "Invalid token payload"}), 401

    access_expires: timedelta = current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]
    access_token = create_access_token(identity=user_id, expires_delta=access_expires)
    return (
        jsonify(
            {
                "access_token": access_token,
                "expires_in": int(access_expires.total_seconds()),
            }
        ),
        200,
    )


@auth_bp.post("/logout")
@jwt_required()
def logout():
    # For this assignment, we mock logout by simply returning success.
    # In a real implementation you would maintain a token blacklist or
    # rotate secrets.
    return jsonify({"message": "Logged out"}), 200

