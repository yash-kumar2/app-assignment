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


def build_masked_stream_url(youtube_id: str) -> str:
    """Return a masked, embed-safe stream URL for the client.

    The YouTube ID is never sent to the client – instead, we generate a stable
    internal URL that could be backed by a proxy or player service.
    """
    # In a real implementation this would be something like:
    #   https://player.yourdomain.com/embed/<opaque-id>
    # where `<opaque-id>` does NOT reveal the YouTube ID.
    opaque = quote(youtube_id, safe="")
    return f"https://player.example.com/embed/{opaque}"

