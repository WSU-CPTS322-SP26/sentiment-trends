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

MASTODON_INSTANCE_URL = os.environ.get("MASTODON_INSTANCE_URL", "https://mastodon.social")
MASTODON_CLIENT_KEY = os.environ.get("MASTODON_CLIENT_KEY")
MASTODON_CLIENT_SECRET = os.environ.get("MASTODON_CLIENT_SECRET")
MASTODON_ACCESS_TOKEN = os.environ.get("MASTODON_ACCESS_TOKEN")