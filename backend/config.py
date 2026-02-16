import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BLUESKY_APP_VIEW_URL = os.environ.get("BLUESKY_APP_VIEW_URL", "https://public.api.bsky.app")
BLUESKY_HANDLE = os.environ.get("BLUESKY_HANDLE")
BLUESKY_APP_PASSWORD = os.environ.get("BLUESKY_APP_PASSWORD")
BLUESKY_SESSION_STRING = os.environ.get("BLUESKY_SESSION_STRING") # leave empty for now