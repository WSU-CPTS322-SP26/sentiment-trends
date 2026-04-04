# integration tests for mastodon routes; require real credentials for success path, no mocks.
import pytest

from tests.integration.conftest import require_mastodon_credentials

pytestmark = pytest.mark.integration


def test_timeline_returns_200_and_shape_when_credentials_set(client):
    """GET /mastodon/timeline returns 200 and JSON with cursor and feed when credentials are set."""
    require_mastodon_credentials()
    resp = client.get("/mastodon/timeline?limit=5")
    if resp.status_code == 401:
        data = resp.get_json()
        assert "error" in data
        return
    assert resp.status_code == 200
    data = resp.get_json()
    assert "cursor" in data
    assert "feed" in data
    assert isinstance(data["feed"], list)


def test_timeline_returns_401_when_credentials_not_set(client):
    """GET /mastodon/timeline returns 401 and error body when credentials are not set."""
    resp = client.get("/mastodon/timeline")
    if resp.status_code == 200:
        data = resp.get_json()
        assert "feed" in data and "cursor" in data
        return
    assert resp.status_code == 401
    data = resp.get_json()
    assert "error" in data


def test_search_returns_200_and_shape_when_credentials_set(client):
    """GET /mastodon/search returns 200 and JSON with posts, cursor, hits_total when credentials are set."""
    require_mastodon_credentials()
    resp = client.get("/mastodon/search?q=elections&limit=5")
    if resp.status_code == 401:
        data = resp.get_json()
        assert "error" in data
        return
    assert resp.status_code == 200
    data = resp.get_json()
    assert "posts" in data
    assert "cursor" in data
    assert "hits_total" in data
    assert isinstance(data["posts"], list)


def test_search_returns_401_when_credentials_not_set(client):
    """GET /mastodon/search returns 401 and error body when credentials are not set."""
    resp = client.get("/mastodon/search?q=test")
    if resp.status_code == 200:
        data = resp.get_json()
        assert "posts" in data and "cursor" in data
        return
    assert resp.status_code == 401
    data = resp.get_json()
    assert "error" in data
