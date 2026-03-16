# API layer tests for apis.bluesky; config and atproto Client are mocked.
from unittest.mock import MagicMock, patch

import apis.bluesky as bluesky


def test_authenticated_client_returns_error_when_no_credentials():
    """_authenticated_client returns (None, msg) when no Bluesky credentials set."""
    with patch("apis.bluesky.config") as mock_cfg:
        mock_cfg.BLUESKY_SESSION_STRING = None
        mock_cfg.BLUESKY_HANDLE = None
        mock_cfg.BLUESKY_APP_PASSWORD = None
        result = bluesky._authenticated_client()
    assert result[0] is None
    assert "Credentials not set" in result[1]


def test_authenticated_client_returns_error_when_login_raises():
    """_authenticated_client returns (None, str(e)) when login raises."""
    with patch("apis.bluesky.Client") as MockClient:
        with patch("apis.bluesky.config") as mock_cfg:
            mock_cfg.BLUESKY_SESSION_STRING = None
            mock_cfg.BLUESKY_HANDLE = "user"
            mock_cfg.BLUESKY_APP_PASSWORD = "pass"
            mock_instance = MagicMock()
            mock_instance.login.side_effect = Exception("login failed")
            MockClient.return_value = mock_instance
            result = bluesky._authenticated_client()
    assert result[0] is None
    assert result[1] == "login failed"


def test_authenticated_client_returns_client_when_handle_password_set():
    """_authenticated_client returns (client, None) when handle and app password work."""
    with patch("apis.bluesky.Client") as MockClient:
        with patch("apis.bluesky.config") as mock_cfg:
            mock_cfg.BLUESKY_SESSION_STRING = None
            mock_cfg.BLUESKY_HANDLE = "user"
            mock_cfg.BLUESKY_APP_PASSWORD = "pass"
            mock_instance = MagicMock()
            MockClient.return_value = mock_instance
            result = bluesky._authenticated_client()
    assert result[0] is mock_instance
    assert result[1] is None


def test_get_timeline_auth_failure_returns_error_tuple():
    """get_timeline returns (None, err) when _authenticated_client returns no client."""
    with patch("apis.bluesky._authenticated_client") as mock_auth:
        mock_auth.return_value = (None, "Auth failed")
        result = bluesky.get_timeline()
    assert result == (None, "Auth failed")


def test_get_timeline_success_returns_cursor_and_feed():
    """get_timeline returns dict with cursor and feed when client returns timeline."""
    mock_client = MagicMock()
    mock_resp = MagicMock()
    mock_resp.feed = [{"uri": "at://did:plc:xyz/post/1"}]
    mock_resp.cursor = "next_cursor"
    mock_client.get_timeline.return_value = mock_resp
    with patch("apis.bluesky._authenticated_client") as mock_auth:
        mock_auth.return_value = (mock_client, None)
        result = bluesky.get_timeline(limit=10, cursor="cur")
    assert result["cursor"] == "next_cursor"
    assert result["feed"] == [{"uri": "at://did:plc:xyz/post/1"}]
    mock_client.get_timeline.assert_called_once_with(
        algorithm="reverse-chronological", cursor="cur", limit=10
    )


def test_get_timeline_invalid_limit_clamped_to_50():
    """get_timeline clamps limit to 50 when limit is out of 1–100."""
    mock_client = MagicMock()
    mock_resp = MagicMock()
    mock_resp.feed = []
    mock_resp.cursor = None
    mock_client.get_timeline.return_value = mock_resp
    with patch("apis.bluesky._authenticated_client") as mock_auth:
        mock_auth.return_value = (mock_client, None)
        bluesky.get_timeline(limit=0)
    mock_client.get_timeline.assert_called_once_with(
        algorithm="reverse-chronological", cursor=None, limit=50
    )


def test_get_timeline_exception_returns_error_tuple():
    """get_timeline returns (None, str(e)) when get_timeline raises."""
    mock_client = MagicMock()
    mock_client.get_timeline.side_effect = Exception("network error")
    with patch("apis.bluesky._authenticated_client") as mock_auth:
        mock_auth.return_value = (mock_client, None)
        result = bluesky.get_timeline()
    assert result[0] is None
    assert result[1] == "network error"


def test_search_posts_empty_q_returns_empty_structure():
    """search_posts returns empty posts/cursor/hits_total when q is empty or whitespace."""
    result = bluesky.search_posts("")
    assert result == {"posts": [], "cursor": None, "hits_total": None}
    result2 = bluesky.search_posts("   ")
    assert result2 == {"posts": [], "cursor": None, "hits_total": None}


def test_search_posts_auth_failure_returns_error_tuple():
    """search_posts returns (None, err) when _authenticated_client returns no client."""
    with patch("apis.bluesky._authenticated_client") as mock_auth:
        mock_auth.return_value = (None, "Auth failed")
        result = bluesky.search_posts("q")
    assert result == (None, "Auth failed")


def test_search_posts_success_returns_posts_cursor_hits_total():
    """search_posts returns dict with posts, cursor, hits_total when client succeeds."""
    mock_client = MagicMock()
    mock_resp = MagicMock()
    mock_resp.posts = [{"id": "1"}]
    mock_resp.cursor = "next"
    mock_resp.hits_total = 1
    mock_client.app.bsky.feed.search_posts.return_value = mock_resp
    with patch("apis.bluesky._authenticated_client") as mock_auth:
        mock_auth.return_value = (mock_client, None)
        result = bluesky.search_posts("elections", limit=25, cursor="cur", sort="latest")
    assert "posts" in result
    assert result["cursor"] == "next"
    assert result["hits_total"] == 1
    mock_client.app.bsky.feed.search_posts.assert_called_once()
    call_params = mock_client.app.bsky.feed.search_posts.call_args[0][0]
    assert call_params["q"] == "elections"
    assert call_params["limit"] == 25
    assert call_params["cursor"] == "cur"
    assert call_params["sort"] == "latest"


def test_search_posts_exception_returns_error_tuple():
    """search_posts returns (None, str(e)) when search_posts raises."""
    mock_client = MagicMock()
    mock_client.app.bsky.feed.search_posts.side_effect = Exception("timeout")
    with patch("apis.bluesky._authenticated_client") as mock_auth:
        mock_auth.return_value = (mock_client, None)
        result = bluesky.search_posts("q")
    assert result[0] is None
    assert result[1] == "timeout"
