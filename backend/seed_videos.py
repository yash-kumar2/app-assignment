"""
Seed script for inserting sample videos into MongoDB.

Run:
    export FLASK_ENV=development
    cp .env.example .env  # then edit values
    pip install -r requirements.txt
    python seed_videos.py
"""

import os

from dotenv import load_dotenv

from config import Config
from extensions.db import init_db, get_db
from app import create_app


def seed():
    load_dotenv()
    app = create_app(Config)
    with app.app_context():
        init_db(app)
        db = get_db()

        videos = [
            {
                "title": "How Startups Fail",
                "description": "Lessons from real founders.",
                "youtube_id": "dQw4w9WgXcQ",
                "thumbnail_url": "https://img.youtube.com/vi/dQw4w9WgXcQ/hqdefault.jpg",
                "is_active": True,
            },
            {
                "title": "Scaling Engineering Teams",
                "description": "Strategies to grow from 5 to 50 engineers.",
                "youtube_id": "L_jWHffIx5E",
                "thumbnail_url": "https://img.youtube.com/vi/L_jWHffIx5E/hqdefault.jpg",
                "is_active": True,
            },
            {
                "title": "Founder Mindset",
                "description": "How to think like a founder.",
                "youtube_id": "9bZkp7q19f0",
                "thumbnail_url": "https://img.youtube.com/vi/9bZkp7q19f0/hqdefault.jpg",
                "is_active": True,
            },
        ]

        if db["videos"].count_documents({}) == 0:
            db["videos"].insert_many(videos)
            print(f"Inserted {len(videos)} videos.")
        else:
            print("Videos collection already has data; skipping.")


if __name__ == "__main__":
    seed()

