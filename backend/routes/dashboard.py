from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from models.video import Video

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.get("/dashboard")
@jwt_required()
def dashboard():
    """Return exactly two active videos for the dashboard."""
    videos = Video.find_active_dashboard_videos(limit=2)
    return jsonify({"videos": [v.to_public_dict() for v in videos]})

