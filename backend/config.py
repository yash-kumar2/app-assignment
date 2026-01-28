import os
from datetime import timedelta


class Config:
    """Base configuration loaded from environment variables.

    All secrets must be provided via environment, not committed.
    """

    # Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")

    # MongoDB
    MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/video_app")
    MONGODB_DB_NAME = os.environ.get("MONGODB_DB_NAME", "video_app")

    # JWT (for auth access/refresh tokens)
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-jwt-secret-change-me")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES", "3600"))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(os.environ.get("JWT_REFRESH_TOKEN_EXPIRES_DAYS", "7"))
    )

    # Playback token settings (separate logical concern, but can reuse JWT secret)
    PLAYBACK_TOKEN_SECRET = os.environ.get("PLAYBACK_TOKEN_SECRET", JWT_SECRET_KEY)
    PLAYBACK_TOKEN_EXPIRES_SECONDS = int(
        os.environ.get("PLAYBACK_TOKEN_EXPIRES_SECONDS", "300")
    )  # <= 5 minutes

    # Rate limiting (for login endpoint)
    RATELIMIT_STORAGE_URI = os.environ.get(
        "RATELIMIT_STORAGE_URI", "memory://"
    )  # for dev; in prod use redis
    LOGIN_RATE_LIMIT = os.environ.get("LOGIN_RATE_LIMIT", "5 per minute")

