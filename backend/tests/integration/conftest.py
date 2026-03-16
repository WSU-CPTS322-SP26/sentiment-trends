# shared fixtures and skip helpers for integration tests; require real credentials when running real tests.
import pytest

import config


def bluesky_credentials_available() -> bool:
    """True if Bluesky credentials are set (session string or handle + app password)."""
    if config.BLUESKY_SESSION_STRING:
        return True
    return bool(config.BLUESKY_HANDLE and config.BLUESKY_APP_PASSWORD)


def mastodon_credentials_available() -> bool:
    """True if Mastodon credentials are set (access token and client keys)."""
    return bool(
        config.MASTODON_ACCESS_TOKEN
        and config.MASTODON_CLIENT_KEY
        and config.MASTODON_CLIENT_SECRET
    )


def require_bluesky_credentials():
    """Skip the test when Bluesky credentials are not set."""
    if not bluesky_credentials_available():
        pytest.skip("Bluesky credentials not set; set BLUESKY_HANDLE and BLUESKY_APP_PASSWORD or BLUESKY_SESSION_STRING")


def require_mastodon_credentials():
    """Skip the test when Mastodon credentials are not set."""
    if not mastodon_credentials_available():
        pytest.skip("Mastodon credentials not set; set MASTODON_* in .env")
