from bson import ObjectId

from extensions.db import get_db


class Video:
    """Video model wrapping YouTube IDs which are never exposed to the client."""

    collection_name = "videos"

    def __init__(self, data: dict):
        self.data = data

    @classmethod
    def collection(cls):
        return get_db()[cls.collection_name]

    @classmethod
    def find_active_dashboard_videos(cls, limit: int = 2):
        cursor = (
            cls.collection()
            .find({"is_active": True})
            .sort("_id", -1)
            .limit(limit)
        )
        return [cls(doc) for doc in cursor]

    @classmethod
    def find_by_id(cls, video_id: str):
        try:
            oid = ObjectId(video_id)
        except Exception:
            return None
        doc = cls.collection().find_one({"_id": oid, "is_active": True})
        return cls(doc) if doc else None

    def to_public_dict(self) -> dict:
        """Public representation without leaking YouTube implementation details."""
        return {
            "id": str(self.data["_id"]),
            "title": self.data.get("title"),
            "description": self.data.get("description"),
            "thumbnail_url": self.data.get("thumbnail_url"),
        }

    def get_youtube_id(self) -> str:
        """Internal accessor. Never send to client."""
        return self.data["youtube_id"]

