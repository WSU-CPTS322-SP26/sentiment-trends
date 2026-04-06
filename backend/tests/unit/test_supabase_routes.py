# unit tests for supabase routes; mock db layer only.
from unittest.mock import patch

import pytest

pytestmark = pytest.mark.unit


def test_homepage_returns_200_and_cards(client):
    """GET /supabase/home returns json with cards from get_homepage_topics."""
    sample = [
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "title": "Bitcoin",
            "category": ["Finance"],
            "searches": 1000,
            "increase_pct": 12,
            "positive_pct": 40.0,
            "neutral_pct": 35.0,
            "negative_pct": 25.0,
            "snapshot_at": "2026-04-01T12:00:00+00:00",
        }
    ]
    with patch("routes.supabase_routes.get_homepage_topics", return_value=sample):
        resp = client.get("/supabase/home")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data == {"cards": sample}


def test_homepage_500_when_db_raises(client):
    """GET /supabase/home returns 500 when get_homepage_topics raises."""
    with patch(
        "routes.supabase_routes.get_homepage_topics",
        side_effect=RuntimeError("supabase down"),
    ):
        resp = client.get("/supabase/home")
    assert resp.status_code == 500
    assert resp.get_json() == {"error": "supabase down"}


def test_topic_detail_400_without_params(client):
    resp = client.get("/supabase/topic")
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_topic_detail_404_when_not_found(client):
    with patch("routes.supabase_routes.get_topic_detail_by_name", return_value=None):
        resp = client.get("/supabase/topic?topic=nope")
    assert resp.status_code == 404
    assert resp.get_json() == {"error": "topic not found"}


def test_topic_detail_200_by_topic_param(client):
    payload = {"topic": {"id": "1", "title": "Alpha"}, "posts": []}
    with patch("routes.supabase_routes.get_topic_detail_by_name", return_value=payload) as m:
        resp = client.get("/supabase/topic?topic=Alpha")
    assert resp.status_code == 200
    assert resp.get_json() == payload
    m.assert_called_once_with("Alpha")


def test_topic_detail_200_by_id_prefers_id(client):
    payload = {"topic": {"id": "550e8400-e29b-41d4-a716-446655440000"}, "posts": []}
    with patch("routes.supabase_routes.get_topic_detail_by_id", return_value=payload) as m_id:
        with patch("routes.supabase_routes.get_topic_detail_by_name") as m_name:
            resp = client.get(
                "/supabase/topic?id=550e8400-e29b-41d4-a716-446655440000&topic=Other"
            )
    assert resp.status_code == 200
    assert resp.get_json() == payload
    m_id.assert_called_once_with("550e8400-e29b-41d4-a716-446655440000")
    m_name.assert_not_called()


def test_topic_detail_500_when_db_raises(client):
    with patch(
        "routes.supabase_routes.get_topic_detail_by_name",
        side_effect=RuntimeError("supabase down"),
    ):
        resp = client.get("/supabase/topic?q=x")
    assert resp.status_code == 500
    assert resp.get_json() == {"error": "supabase down"}
