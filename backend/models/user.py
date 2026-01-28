from datetime import datetime

from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

from extensions.db import get_db


class User:
    """User model backed by MongoDB.

    This is a thin wrapper around the underlying collection to keep all user-related
    persistence logic on the backend.
    """

    collection_name = "users"

    def __init__(self, data: dict):
        self.data = data

    @classmethod
    def collection(cls):
        return get_db()[cls.collection_name]

    @classmethod
    def create(cls, name: str, email: str, password: str):
        now = datetime.utcnow()
        password_hash = generate_password_hash(password)
        doc = {
            "name": name,
            "email": email.lower(),
            "password_hash": password_hash,
            "created_at": now,
        }
        result = cls.collection().insert_one(doc)
        doc["_id"] = result.inserted_id
        return cls(doc)

    @classmethod
    def find_by_email(cls, email: str):
        doc = cls.collection().find_one({"email": email.lower()})
        return cls(doc) if doc else None

    @classmethod
    def find_by_id(cls, user_id: str):
        try:
            oid = ObjectId(user_id)
        except Exception:
            return None
        doc = cls.collection().find_one({"_id": oid})
        return cls(doc) if doc else None

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.data["password_hash"], password)

    def to_public_dict(self) -> dict:
        return {
            "id": str(self.data["_id"]),
            "name": self.data["name"],
            "email": self.data["email"],
            "created_at": self.data["created_at"].isoformat() + "Z",
        }

