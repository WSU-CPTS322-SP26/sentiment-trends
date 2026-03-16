# unit tests for app index route; mock only.
import pytest

pytestmark = pytest.mark.unit


def test_index_returns_200(client):
    """GET / returns 200 and backend running message."""
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data == {"message": "Backend is running"}
