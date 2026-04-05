# unit tests for supabase routes; mock db layer only.
from unittest.mock import patch

import pytest

pytestmark = pytest.mark.unit


def test_homepage_returns_200_and_cards(client):
    """GET /supabase/homepage returns json with cards from get_homepage_topics."""
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
        resp = client.get("/supabase/homepage")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data == {"cards": sample}


def test_homepage_500_when_db_raises(client):
    """GET /supabase/homepage returns 500 when get_homepage_topics raises."""
    with patch(
        "routes.supabase_routes.get_homepage_topics",
        side_effect=RuntimeError("supabase down"),
    ):
        resp = client.get("/supabase/homepage")
    assert resp.status_code == 500
    assert resp.get_json() == {"error": "supabase down"}
