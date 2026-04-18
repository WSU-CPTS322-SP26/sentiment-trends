# unit tests for db.homepage helpers; mock supabase client.
from unittest.mock import MagicMock, patch

import pytest

from db import homepage

pytestmark = pytest.mark.unit


def test_pick_latest_sentiment_empty():
    assert homepage._pick_latest_sentiment(None) is None
    assert homepage._pick_latest_sentiment([]) is None


def test_pick_latest_sentiment_max_created_at():
    rows = [
        {"pos_pct": 10.0, "created_at": "2026-04-01T00:00:00+00:00"},
        {"pos_pct": 50.0, "created_at": "2026-04-03T00:00:00+00:00"},
        {"pos_pct": 20.0, "created_at": "2026-04-02T00:00:00+00:00"},
    ]
    latest = homepage._pick_latest_sentiment(rows)
    assert latest["pos_pct"] == 50.0


def test_get_homepage_topics_maps_rows():
    """Supabase response is mapped to card dicts with latest sentiment."""
    mock_row = {
        "id": "11111111-1111-1111-1111-111111111111",
        "name": "Alpha",
        "category": ["Tech"],
        "searches": 99,
        "increase_pct": 5,
        "daily_topic_sentiment": [
            {
                "pos_pct": 1.0,
                "neu_pct": 2.0,
                "neg_pct": 3.0,
                "avg_compound": 0.1,
                "created_at": "2026-01-01T00:00:00Z",
            },
            {
                "pos_pct": 10.0,
                "neu_pct": 20.0,
                "neg_pct": 70.0,
                "avg_compound": -0.42,
                "created_at": "2026-06-01T00:00:00Z",
            },
        ],
        "image_url": [
            "https://example.com/a.jpg",
            "https://example.com/b.jpg",
        ],
    }
    mock_execute = MagicMock()
    mock_execute.execute.return_value = MagicMock(data=[mock_row])

    mock_chain = MagicMock()
    mock_chain.select.return_value = mock_chain
    mock_chain.order.return_value = mock_execute

    mock_table = MagicMock(return_value=mock_chain)

    with patch("db.homepage.config") as cfg:
        cfg.supabase.table = mock_table
        cards = homepage.get_homepage_topics()

    mock_table.assert_called_once_with("topics")
    assert len(cards) == 1
    c = cards[0]
    assert c["id"] == "11111111-1111-1111-1111-111111111111"
    assert c["title"] == "Alpha"
    assert c["category"] == ["Tech"]
    assert c["searches"] == 99
    assert c["increase_pct"] == 5
    assert c["positive_pct"] == 10.0
    assert c["neutral_pct"] == 20.0
    assert c["negative_pct"] == 70.0
    assert c["avg_compound"] == -0.42
    assert c["snapshot_at"] == "2026-06-01T00:00:00Z"
    assert c["image_url"] == [
        "https://example.com/a.jpg",
        "https://example.com/b.jpg",
    ]


def test_get_homepage_topics_no_sentiment_rows():
    mock_row = {
        "id": "22222222-2222-2222-2222-222222222222",
        "name": "Beta",
        "category": None,
        "searches": None,
        "increase_pct": None,
        "daily_topic_sentiment": [],
    }
    mock_execute = MagicMock()
    mock_execute.execute.return_value = MagicMock(data=[mock_row])

    mock_chain = MagicMock()
    mock_chain.select.return_value = mock_chain
    mock_chain.order.return_value = mock_execute

    with patch("db.homepage.config") as cfg:
        cfg.supabase.table = MagicMock(return_value=mock_chain)
        cards = homepage.get_homepage_topics()

    c = cards[0]
    assert c["positive_pct"] is None
    assert c["neutral_pct"] is None
    assert c["negative_pct"] is None
    assert c["avg_compound"] is None
    assert c["snapshot_at"] is None
    assert c["image_url"] is None
