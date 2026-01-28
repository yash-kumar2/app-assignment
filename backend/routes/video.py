from datetime import datetime

import requests
from flask import Blueprint, jsonify, request, Response, stream_with_context
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions.db import get_db
from models.video import Video
from utils.token import generate_playback_token, verify_playback_token
from utils.youtube import get_video_upstream_url

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

    # Resolve upstream URL
    youtube_id = video.get_youtube_id()
    upstream_url = get_video_upstream_url(youtube_id)

    # Proxy the stream
    headers = {}
    if "Range" in request.headers:
        headers["Range"] = request.headers["Range"]

    req = requests.get(upstream_url, headers=headers, stream=True)

    excluded_headers = [
        "content-encoding",
        "content-length",
        "transfer-encoding",
        "connection",
    ]
    headers_to_forward = [
        (k, v)
        for k, v in req.headers.items()
        if k.lower() not in excluded_headers
    ]

    response = Response(
        stream_with_context(req.iter_content(chunk_size=1024 * 1024)),
        status=req.status_code,
        headers=headers_to_forward,
    )
    
    # Explicitly set Content-Length if available from upstream
    if "Content-Length" in req.headers:
        response.headers["Content-Length"] = req.headers["Content-Length"]
        
    return response


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

