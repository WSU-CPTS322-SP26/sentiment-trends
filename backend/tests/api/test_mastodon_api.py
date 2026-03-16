# API layer tests for apis.mastodon; config and Mastodon client are mocked. Marked unit.
import pytest
from unittest.mock import MagicMock, patch

import apis.mastodon as mastodon

pytestmark = pytest.mark.unit


def test_authenticated_client_returns_error_when_no_token():
    """_authenticated_client returns (None, msg) when MASTODON_ACCESS_TOKEN is missing."""
    with patch("apis.mastodon.config") as mock_cfg:
        mock_cfg.MASTODON_ACCESS_TOKEN = None
        result = mastodon._authenticated_client()
    assert result[0] is None
    assert "Credentials not set" in result[1]


def test_authenticated_client_returns_error_when_verify_raises():
    """_authenticated_client returns (None, str(e)) when account_verify_credentials raises."""
    with patch("apis.mastodon.Mastodon") as MockMastodon:
        with patch("apis.mastodon.config") as mock_cfg:
            mock_cfg.MASTODON_ACCESS_TOKEN = "t"
            mock_cfg.MASTODON_CLIENT_KEY = "k"
            mock_cfg.MASTODON_CLIENT_SECRET = "s"
            mock_cfg.MASTODON_INSTANCE_URL = "https://mastodon.social"
            mock_instance = MagicMock()
            mock_instance.account_verify_credentials.side_effect = Exception("bad token")
            MockMastodon.return_value = mock_instance
            result = mastodon._authenticated_client()
    assert result[0] is None
    assert result[1] == "bad token"


def test_authenticated_client_returns_client_when_success():
    """_authenticated_client returns (client, None) when credentials work."""
    with patch("apis.mastodon.Mastodon") as MockMastodon:
        with patch("apis.mastodon.config") as mock_cfg:
            mock_cfg.MASTODON_ACCESS_TOKEN = "t"
            mock_cfg.MASTODON_CLIENT_KEY = "k"
            mock_cfg.MASTODON_CLIENT_SECRET = "s"
            mock_cfg.MASTODON_INSTANCE_URL = "https://mastodon.social"
            mock_instance = MagicMock()
            MockMastodon.return_value = mock_instance
            result = mastodon._authenticated_client()
    assert result[0] is mock_instance
    assert result[1] is None


def test_get_timeline_auth_failure_returns_error_tuple():
    """get_timeline returns (None, err) when _authenticated_client returns no client."""
    with patch("apis.mastodon._authenticated_client") as mock_auth:
        mock_auth.return_value = (None, "Auth failed")
        result = mastodon.get_timeline()
    assert result == (None, "Auth failed")


def test_get_timeline_success_returns_cursor_and_feed():
    """get_timeline returns dict with cursor and feed when client returns statuses."""
    mock_client = MagicMock()
    mock_client.timeline_home.return_value = [{"id": "next_id"}]
    with patch("apis.mastodon._authenticated_client") as mock_auth:
        mock_auth.return_value = (mock_client, None)
        result = mastodon.get_timeline(limit=10, cursor="max_id")
    assert result == {"cursor": "next_id", "feed": [{"id": "next_id"}]}
    mock_client.timeline_home.assert_called_once_with(limit=10, max_id="max_id")


def test_get_timeline_invalid_limit_clamped_to_50():
    """get_timeline clamps limit to 50 when limit is out of 1–100."""
    mock_client = MagicMock()
    mock_client.timeline_home.return_value = []
    with patch("apis.mastodon._authenticated_client") as mock_auth:
        mock_auth.return_value = (mock_client, None)
        mastodon.get_timeline(limit=0)
    mock_client.timeline_home.assert_called_once_with(limit=50, max_id=None)


def test_get_timeline_exception_returns_error_tuple():
    """get_timeline returns (None, str(e)) when timeline_home raises."""
    mock_client = MagicMock()
    mock_client.timeline_home.side_effect = Exception("network error")
    with patch("apis.mastodon._authenticated_client") as mock_auth:
        mock_auth.return_value = (mock_client, None)
        result = mastodon.get_timeline()
    assert result[0] is None
    assert result[1] == "network error"


def test_search_posts_empty_q_returns_empty_structure():
    """search_posts returns empty posts/cursor/hits_total when q is empty or whitespace."""
    result = mastodon.search_posts("")
    assert result == {"posts": [], "cursor": None, "hits_total": None}
    result2 = mastodon.search_posts("   ")
    assert result2 == {"posts": [], "cursor": None, "hits_total": None}


def test_search_posts_auth_failure_returns_error_tuple():
    """search_posts returns (None, err) when _authenticated_client returns no client."""
    with patch("apis.mastodon._authenticated_client") as mock_auth:
        mock_auth.return_value = (None, "Auth failed")
        result = mastodon.search_posts("q")
    assert result == (None, "Auth failed")


def test_search_posts_success_returns_posts_cursor_hits_total():
    """search_posts returns dict with posts, cursor, hits_total when client succeeds."""
    mock_client = MagicMock()
    mock_client.search_v2.return_value = {"statuses": [{"id": "1", "content": "hi"}]}
    with patch("apis.mastodon._authenticated_client") as mock_auth:
        mock_auth.return_value = (mock_client, None)
        result = mastodon.search_posts("elections", cursor="0", limit=25)
    assert "posts" in result
    assert "cursor" in result
    assert "hits_total" in result
    assert len(result["posts"]) == 1
    mock_client.search_v2.assert_called_once_with("elections", result_type="statuses", offset=0)


def test_search_posts_exception_returns_error_tuple():
    """search_posts returns (None, str(e)) when search_v2 raises."""
    mock_client = MagicMock()
    mock_client.search_v2.side_effect = Exception("timeout")
    with patch("apis.mastodon._authenticated_client") as mock_auth:
        mock_auth.return_value = (mock_client, None)
        result = mastodon.search_posts("q")
    assert result[0] is None
    assert result[1] == "timeout"
