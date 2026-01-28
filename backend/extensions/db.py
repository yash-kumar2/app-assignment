from flask import current_app
from pymongo import MongoClient


mongo_client: MongoClient | None = None
db = None


def init_db(app):
    """Initialize a global MongoDB client and database handle."""
    global mongo_client, db

    uri = app.config["MONGODB_URI"]
    db_name = app.config["MONGODB_DB_NAME"]

    mongo_client = MongoClient(uri)
    db = mongo_client[db_name]


def get_db():
    """Get the active database handle."""
    if db is None:
        # This should not happen if init_db is called from app factory
        raise RuntimeError("Database not initialized. Call init_db(app) first.")
    return db

