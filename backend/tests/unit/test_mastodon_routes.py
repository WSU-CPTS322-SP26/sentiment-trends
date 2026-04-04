# unit tests for mastodon routes; API layer is mocked.
import pytest
from unittest.mock import patch

pytestmark = pytest.mark.unit

# request: GET /mastodon/timeline and /mastodon/search; mock apis.mastodon so no real calls.
@patch("routes.mastodon_routes.mastodon")
def test_timeline_returns_200_when_api_returns_success(mock_mastodon, client):
    """timeline returns 200 and JSON when get_timeline returns a dict."""
    mock_mastodon.get_timeline.return_value = {"cursor": "next", "feed": [{"id": "1"}]}
    resp = client.get("/mastodon/timeline?limit=10&cursor=abc")
    assert resp.status_code == 200
    assert resp.get_json() == {"cursor": "next", "feed": [{"id": "1"}]}
    mock_mastodon.get_timeline.assert_called_once_with(limit=10, cursor="abc")


@patch("routes.mastodon_routes.mastodon")
def test_timeline_returns_401_when_api_returns_error(mock_mastodon, client):
    """timeline returns 401 and error body when get_timeline returns (None, msg)."""
    mock_mastodon.get_timeline.return_value = (None, "Credentials not set")
    resp = client.get("/mastodon/timeline")
    assert resp.status_code == 401
    assert resp.get_json() == {"error": "Credentials not set"}


@patch("routes.mastodon_routes.mastodon")
def test_timeline_returns_401_when_api_raises(mock_mastodon, client):
    """timeline returns 401 when get_timeline raises."""
    mock_mastodon.get_timeline.side_effect = RuntimeError("network error")
    resp = client.get("/mastodon/timeline")
    assert resp.status_code == 401
    assert "error" in resp.get_json()


@patch("routes.mastodon_routes.mastodon")
def test_search_returns_200_when_api_returns_success(mock_mastodon, client):
    """search returns 200 and JSON when search_posts returns a dict."""
    mock_mastodon.search_posts.return_value = {"posts": [], "cursor": None, "hits_total": 0}
    resp = client.get("/mastodon/search?topic=elections&limit=25")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["posts"] == []
    mock_mastodon.search_posts.assert_called_once()
    call_kw = mock_mastodon.search_posts.call_args[1]
    assert call_kw["limit"] == 25
    assert call_kw["sort"] == "latest"


@patch("routes.mastodon_routes.mastodon")
def test_search_topic_takes_precedence_over_q(mock_mastodon, client):
    """search uses topic when both topic and q are present."""
    mock_mastodon.search_posts.return_value = {"posts": [], "cursor": None, "hits_total": None}
    client.get("/mastodon/search?topic=foo&q=bar")
    mock_mastodon.search_posts.assert_called_once_with("foo", limit=None, cursor=None, sort="latest", tag=None)


@patch("routes.mastodon_routes.mastodon")
def test_search_parses_tag_comma_list(mock_mastodon, client):
    """search parses tag=a,b,c into list and trims spaces."""
    mock_mastodon.search_posts.return_value = {"posts": [], "cursor": None, "hits_total": None}
    client.get("/mastodon/search?q=x&tag=a,%20b%20,%20c")
    call_kw = mock_mastodon.search_posts.call_args[1]
    assert call_kw["tag"] == ["a", "b", "c"]


@patch("routes.mastodon_routes.mastodon")
def test_search_returns_401_when_api_returns_error(mock_mastodon, client):
    """search returns 401 when search_posts returns (None, msg)."""
    mock_mastodon.search_posts.return_value = (None, "Auth failed")
    resp = client.get("/mastodon/search?q=test")
    assert resp.status_code == 401
    assert resp.get_json() == {"error": "Auth failed"}


@patch("routes.mastodon_routes.mastodon")
def test_search_returns_401_when_api_raises(mock_mastodon, client):
    """search returns 401 when search_posts raises."""
    mock_mastodon.search_posts.side_effect = Exception("timeout")
    resp = client.get("/mastodon/search?q=test")
    assert resp.status_code == 401
    assert "error" in resp.get_json()
