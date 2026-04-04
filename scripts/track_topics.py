"""
CLI: fetch Google Trends topics, analyze sentiment across Bluesky/Mastodon,
and persist to Supabase (topics, daily_topic_sentiment, top_posts).

Run from repo root: python scripts/track_topics.py
Requires backend deps (pip install -r backend/requirements.txt) and env vars
(SUPABASE_URL, SUPABASE_SERVICE_KEY, SERPAPI_KEY, Bluesky/Mastodon as needed).
"""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

# Defaults — change here to adjust script-wide defaults without CLI flags.
DEFAULT_MAX_TOPICS = 100
DEFAULT_BLUESKY_LIMIT = 500
DEFAULT_MASTODON_LIMIT = 100
DEFAULT_TOP_N = 5

_REPO_ROOT = Path(__file__).resolve().parents[1]
_BACKEND = _REPO_ROOT / "backend"
# so `import config` and backend packages resolve when run from scripts/
if str(_BACKEND) not in sys.path:
    sys.path.insert(0, str(_BACKEND))

try:
    from dotenv import load_dotenv

    load_dotenv(_BACKEND / ".env")
except ImportError:
    pass  # optional dep; env may already be set

import config  # noqa: E402 — after sys.path
from apis.topics import get_trending_now  # noqa: E402
from services.sentiment import analyze_topic  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)


def _to_int(value: object) -> int | None:
    """Parse ints from messy API values (e.g. strings with %, commas).

    Returns:
        int if coercible, else None. Booleans are ignored (not treated as 0/1).
    """
    if value is None:
        return None
    if isinstance(value, bool):
        return None  # don't treat True/False as 1/0
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        s = value.strip().replace("%", "").replace("+", "").replace(",", "")
        if not s:
            return None
        try:
            return int(float(s))
        except ValueError:
            return None
    return None


def _normalize_categories(raw: object) -> list[str] | None:
    """Flatten category data from the trends API into a list of strings.

    Returns:
        Non-empty list of stripped names, or None if nothing usable.
    """
    if raw is None:
        return None
    if isinstance(raw, str):
        return [raw] if raw.strip() else None
    if not isinstance(raw, (list, tuple)):
        return None
    out: list[str] = []
    for item in raw:
        if isinstance(item, str) and item.strip():
            out.append(item.strip())
        elif isinstance(item, dict):
            # nested objects sometimes use different field names
            for key in ("name", "label", "title", "category"):
                v = item.get(key)
                if isinstance(v, str) and v.strip():
                    out.append(v.strip())
                    break
    return out or None


def _upsert_topic_row(topic_row: dict) -> str:
    """Upsert one trending topic into `topics` (by name) and return its id.

    Args:
        topic_row: dict with at least `query`; optional search_volume, increase_percentage, categories.

    Returns:
        Topic id as string (for foreign keys).

    Raises:
        ValueError: missing query/name.
        RuntimeError: could not read id after upsert/select.
    """
    name = (topic_row.get("query") or "").strip()
    if not name:
        raise ValueError("topic row missing query/name")

    payload: dict = {"name": name}
    sv = _to_int(topic_row.get("search_volume"))
    if sv is not None:
        payload["searches"] = sv
    inc = _to_int(topic_row.get("increase_percentage"))
    if inc is not None:
        payload["increase_pct"] = inc
    cats = _normalize_categories(topic_row.get("categories"))
    if cats is not None:
        payload["category"] = cats

    # postgrest-py 2.x usually returns the row (with id); if not, fetch by name
    res = config.supabase.table("topics").upsert(payload, on_conflict="name").execute()
    rows = res.data or []
    tid = rows[0].get("id") if rows else None
    if not tid:
        sel = (
            config.supabase.table("topics")
            .select("id")
            .eq("name", name)
            .limit(1)
            .execute()
        )
        srows = sel.data or []
        tid = srows[0].get("id") if srows else None
    if not tid:
        raise RuntimeError(f"could not resolve topic id for name={name!r}")
    return str(tid)


def _insert_daily_sentiment(
    *,
    topic_id: str,
    created_at: str,
    unified: dict,
    per_platform: dict,
) -> None:
    """Insert one `daily_topic_sentiment` row (aggregate scores + per-platform post counts).

    Args:
        topic_id: topics.id for this snapshot.
        created_at: ISO timestamp for the batch run.
        unified: keys like positive_pct, neutral_pct, negative_pct.
        per_platform: counts, e.g. bluesky, mastodon.

    Returns:
        None.
    """
    row = {
        "topic_id": topic_id,
        "created_at": created_at,
        "pos_pct": unified.get("positive_pct"),
        "neu_pct": unified.get("neutral_pct"),
        "neg_pct": unified.get("negative_pct"),
        "bluesky_posts": int(per_platform.get("bluesky") or 0),
        "mastodon_posts": int(per_platform.get("mastodon") or 0),
    }
    config.supabase.table("daily_topic_sentiment").insert(row).execute()


def _replace_top_posts(topic_id: str, posts: list[dict]) -> None:
    """Replace all `top_posts` for a topic: delete existing rows, then insert `posts`.

    Skips post dicts without a usable `id`. No-op insert when `posts` is empty after delete.

    Returns:
        None.
    """
    config.supabase.table("top_posts").delete().eq("topic_id", topic_id).execute()
    if not posts:
        return
    rows = []
    for p in posts:
        pid = str(p.get("id") or "").strip()
        if not pid:
            continue  # skip rows we can't key in the db
        url = p.get("url")
        rows.append(
            {
                "id": pid,
                "platform": p.get("platform") or "bluesky",
                "topic_id": topic_id,
                "author": p.get("author"),
                "text": p.get("text"),
                "like_count": int(p.get("like_count") or 0),
                "repost_count": int(p.get("repost_count") or 0),
                "sentiment_label": p.get("label"),
                "sentiment_score": p.get("compound"),
                "url": url if url else None,
            }
        )
    config.supabase.table("top_posts").insert(rows).execute()


def main() -> int:
    """CLI entry: validate args, fetch trending topics, persist each to Supabase.

    Returns:
        0 if the run finished (individual topic failures are logged, not fatal).
        1 for bad CLI args, failed trend fetch, or unexpected API response shape.
    """
    parser = argparse.ArgumentParser(description="Track trending topics into Supabase.")
    parser.add_argument(
        "--max-topics",
        type=int,
        default=DEFAULT_MAX_TOPICS,
        help=f"Max trending topics from SerpAPI (default: {DEFAULT_MAX_TOPICS})",
    )
    parser.add_argument(
        "--bluesky-limit",
        type=int,
        default=DEFAULT_BLUESKY_LIMIT,
        help=f"Bluesky post cap per topic (default: {DEFAULT_BLUESKY_LIMIT})",
    )
    parser.add_argument(
        "--mastodon-limit",
        type=int,
        default=DEFAULT_MASTODON_LIMIT,
        help=f"Mastodon post cap per topic (default: {DEFAULT_MASTODON_LIMIT})",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=DEFAULT_TOP_N,
        help=f"Top posts to store per topic (default: {DEFAULT_TOP_N})",
    )
    args = parser.parse_args()

    # bail early on nonsense limits instead of hitting apis
    if args.max_topics < 1:
        log.error("--max-topics must be >= 1")
        return 1
    if args.bluesky_limit < 1 or args.mastodon_limit < 1:
        log.error("platform limits must be >= 1")
        return 1
    if args.top_n < 1:
        log.error("--top-n must be >= 1")
        return 1

    raw = get_trending_now(max=args.max_topics)
    # get_trending_now returns (None, err) on failure or a dict on success
    if isinstance(raw, tuple) and raw[0] is None:
        log.error("get_trending_now failed: %s", raw[1])
        return 1
    if not isinstance(raw, dict):
        log.error("unexpected get_trending_now response")
        return 1

    topics = raw.get("topics") or []
    # same timestamp for every topic in this run (one batch)
    run_at = datetime.now(timezone.utc).isoformat()

    # each step has its own try so one bad topic doesn't abort the whole run
    for topic_row in topics:
        if not isinstance(topic_row, dict):
            continue
        name = (topic_row.get("query") or "").strip()
        if not name:
            continue

        try:
            topic_id = _upsert_topic_row(topic_row)
        except Exception as e:
            log.exception("upsert topic %r failed: %s", name, e)
            continue

        try:
            analysis = analyze_topic(
                name,
                bluesky_limit=args.bluesky_limit,
                mastodon_limit=args.mastodon_limit,
                top_n=args.top_n,
            )
        except Exception as e:
            log.exception("analyze_topic %r failed: %s", name, e)
            continue

        if analysis.get("errors"):
            log.warning("topic %r analyze warnings: %s", name, analysis["errors"])

        unified = analysis.get("unified") or {}
        per_platform = analysis.get("per_platform_counts") or {}

        try:
            _insert_daily_sentiment(
                topic_id=topic_id,
                created_at=run_at,
                unified=unified,
                per_platform=per_platform,
            )
        except Exception as e:
            log.exception("daily_topic_sentiment insert for %r failed: %s", name, e)
            continue

        try:
            _replace_top_posts(topic_id, analysis.get("top_posts") or [])
        except Exception as e:
            log.exception("top_posts replace for %r failed: %s", name, e)
            continue

        log.info("tracked %r (topic_id=%s)", name, topic_id)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
