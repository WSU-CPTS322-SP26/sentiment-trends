from __future__ import annotations

import config

from db.homepage import _topic_to_card

_TOPICS_SELECT = (
    "id, name, category, searches, increase_pct, "
    "daily_topic_sentiment(pos_pct, neu_pct, neg_pct, avg_compound, created_at, summary), "
    "top_posts(id, platform, author, text, like_count, repost_count, "
    "sentiment_label, sentiment_score, url)"
)


def _post_from_row(row: dict) -> dict:
    """Build one client post dict from a top_posts row."""
    rid = row.get("id")
    return {
        "id": str(rid) if rid is not None else None,
        "platform": row.get("platform"),
        "author": row.get("author"),
        "text": row.get("text"),
        "like_count": row.get("like_count"),
        "repost_count": row.get("repost_count"),
        "label": row.get("sentiment_label"),
        "compound": row.get("sentiment_score"),
        "url": row.get("url"),
    }


def _rows_to_detail(rows: list) -> dict | None:
    """Map a topics query result to topic + posts, or None if empty."""
    if not rows:
        return None
    row = rows[0]
    if not isinstance(row, dict):
        return None
    raw_posts = row.get("top_posts") or []
    posts = [_post_from_row(p) for p in raw_posts if isinstance(p, dict)]
    # stable order: engagement then id
    posts.sort(
        key=lambda p: (
            -(int(p["like_count"] or 0) + int(p["repost_count"] or 0)),
            str(p.get("id") or ""),
        )
    )
    return {"topic": _topic_to_card(row), "posts": posts}


def get_topic_detail_by_id(topic_id: str) -> dict | None:
    """Load one topic with its latest sentiment snapshot and stored top posts.

    Args:
        topic_id: topics.id (uuid string).

    Returns:
        Dict with keys ``topic`` (homepage-style card fields) and ``posts``
        (list of post dicts), or None if no row matches.

    Raises:
        Exception: supabase/postgrest client errors.
    """
    res = (
        config.supabase.table("topics")
        .select(_TOPICS_SELECT)
        .eq("id", topic_id.strip())
        .limit(1)
        .execute()
    )
    return _rows_to_detail(res.data or [])


def get_topic_detail_by_name(name: str) -> dict | None:
    """Load one topic by exact ``topics.name`` with sentiment and top posts.

    Args:
        name: topics.name (matched after strip).

    Returns:
        Dict with keys ``topic`` and ``posts``, or None if no row matches.

    Raises:
        Exception: supabase/postgrest client errors.
    """
    res = (
        config.supabase.table("topics")
        .select(_TOPICS_SELECT)
        .eq("name", name.strip())
        .limit(1)
        .execute()
    )
    return _rows_to_detail(res.data or [])
