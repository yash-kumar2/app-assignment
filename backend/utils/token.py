from datetime import datetime, timedelta, timezone

import jwt
from flask import current_app


def generate_playback_token(video_id: str) -> tuple[str, int]:
    """Generate a short-lived, video-specific signed playback token.

    The token is a compact JWT signed with a backend-only secret. The client
    never sees any YouTube identifiers and can only present this opaque token
    back to the backend.
    """
    expires_in = current_app.config["PLAYBACK_TOKEN_EXPIRES_SECONDS"]
    secret = current_app.config["PLAYBACK_TOKEN_SECRET"]

    now = datetime.now(timezone.utc)
    exp = now + timedelta(seconds=expires_in)

    payload = {
        "sub": "playback",
        "video_id": video_id,
        "exp": exp,
        "iat": now,
    }

    encoded = jwt.encode(payload, secret, algorithm="HS256")
    return encoded, expires_in


def verify_playback_token(token: str, video_id: str) -> bool:
    """Validate that the playback token is valid, unexpired, and video-specific."""
    secret = current_app.config["PLAYBACK_TOKEN_SECRET"]
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False

    if payload.get("sub") != "playback":
        return False
    if payload.get("video_id") != video_id:
        return False
    return True

