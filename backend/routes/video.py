from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions.db import get_db
from models.video import Video
from utils.token import generate_playback_token, verify_playback_token
from utils.youtube import build_masked_stream_url

video_bp = Blueprint("video", __name__)


@video_bp.post("/video/<video_id>/play")
@jwt_required()
def generate_play_token(video_id):
    video = Video.find_by_id(video_id)
    if not video:
        return jsonify({"message": "Video not found"}), 404

    token, expires_in = generate_playback_token(video_id=video_id)
    return (
        jsonify(
            {
                "video_id": video_id,
                "playback_token": token,
                "expires_in": expires_in,
            }
        ),
        200,
    )


@video_bp.get("/video/<video_id>/stream")
@jwt_required()
def stream_video(video_id):
    token = request.args.get("token")
    if not token:
        return jsonify({"message": "Missing playback token"}), 400

    video = Video.find_by_id(video_id)
    if not video:
        return jsonify({"message": "Video not found"}), 404

    # Validate token is short-lived, signed, and matches this video
    if not verify_playback_token(token=token, video_id=video_id):
        return jsonify({"message": "Invalid or expired playback token"}), 403

    # Resolve YouTube ID internally and convert to masked URL
    youtube_id = video.get_youtube_id()
    stream_url = build_masked_stream_url(youtube_id)

    # Never leak the youtube_id or URL directly
    return jsonify({"stream_url": stream_url})


@video_bp.post("/video/<video_id>/watch")
@jwt_required()
def track_watch(video_id):
    """Track watch analytics events (progress, resume, etc.)."""
    user_id = get_jwt_identity()
    video = Video.find_by_id(video_id)
    if not video:
        return jsonify({"message": "Video not found"}), 404

    payload = request.get_json() or {}
    event = payload.get("event")
    timestamp = payload.get("timestamp")

    if event is None or timestamp is None:
        return jsonify({"message": "event and timestamp are required"}), 400

    db = get_db()
    db["watch_events"].insert_one(
        {
            "user_id": user_id,
            "video_id": video_id,
            "event": event,
            "timestamp": timestamp,
            "recorded_at": datetime.utcnow(),
        }
    )

    return jsonify({"message": "Watch event recorded"}), 201

