from __future__ import annotations

import config


def _pick_latest_sentiment(rows: list[dict] | None) -> dict | None:
    """Return the daily_topic_sentiment row with the greatest created_at.

    Args:
        rows: Nested rows from postgrest, or None.

    Returns:
        One dict, or None if there are no rows.
    """
    if not rows:
        return None
    # iso timestamps sorting
    with_ts = [r for r in rows if r.get("created_at") is not None]
    if not with_ts:
        return rows[0]
    return max(with_ts, key=lambda r: str(r["created_at"]))


def _topic_to_card(row: dict) -> dict:
    """Build one homepage card dict from a topics row and nested sentiment rows."""
    latest = _pick_latest_sentiment(row.get("daily_topic_sentiment"))
    return {
        "id": str(row["id"]),
        "title": row["name"],
        "category": row.get("category"),
        "searches": row.get("searches"),
        "increase_pct": row.get("increase_pct"),
        "positive_pct": latest.get("pos_pct") if latest else None,
        "neutral_pct": latest.get("neu_pct") if latest else None,
        "negative_pct": latest.get("neg_pct") if latest else None,
        "avg_compound": latest.get("avg_compound") if latest else None,
        "snapshot_at": latest.get("created_at") if latest else None,
    }


def get_homepage_topics() -> list[dict]:
    """Load all topics with their latest sentiment snapshot for homepage cards.

    Returns:
        List of card dicts: id, title, category, searches, increase_pct,
        positive_pct, neutral_pct, negative_pct (0–100 or null),
        avg_compound (-1..1 or null), snapshot_at.

    Raises:
        Exception: supabase/postgrest client errors.
    """
    res = (
        config.supabase.table("topics")
        .select(
            "id, name, category, searches, increase_pct, "
            "daily_topic_sentiment(pos_pct, neu_pct, neg_pct, avg_compound, created_at)"
        )
        .order("searches", desc=True)
        .execute()
    )
    rows = res.data or []
    return [_topic_to_card(r) for r in rows if isinstance(r, dict)]
