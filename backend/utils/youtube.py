"""
YouTube abstraction layer.

All interaction with YouTube (or any other video provider) must happen through
this module. The rest of the code only deals with internal `Video` models and
never tocuches raw YouTube URLs or IDs directly.

For this assignment we keep it simple and just wrap a fake, masked embed URL.
In a real system this is where you would call the YouTube API, handle API keys,
DRM, etc.
"""

from urllib.parse import quote


def get_video_upstream_url(youtube_id: str) -> str:
    """Return the upstream video source URL for the backend to proxy.

    In a real system, this might generate a signed URL for an S3 bucket or
    fetch a direct stream URL from a provider API.
    """
    # For this assignment, we use a reliable sample video (Big Buck Bunny)
    # because expo-av needs a direct media file (mp4/m3u8), and youtube-dl/
    # yt-dlp is too heavy/unreliable for this simple demo scope.
    return "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"

