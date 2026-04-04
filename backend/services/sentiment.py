from apis import bluesky, mastodon
from utils.helpers import bluesky_uri_to_url, sentiment_label, strip_html, strip_urls
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer  # type: ignore[import-untyped]

sia = SentimentIntensityAnalyzer()

MAX_LIMIT_PER_PLATFORM = 500


def score_post(text: str) -> dict:
    """Run VADER on text; return {compound, label}."""
    clean = strip_urls(text)
    scores = sia.polarity_scores(clean)
    compound = round(scores["compound"], 4)
    return {"compound": compound, "label": sentiment_label(compound)}


def normalize_bluesky_post(post: dict) -> dict | None:
    """Extract fields from a raw Bluesky post dict."""
    try:
        record = post.get("record") or {}
        text = (record.get("text") or "").strip()
        if not text:
            return None
        author_obj = post.get("author") or {}
        handle = author_obj.get("handle") or author_obj.get("did") or "unknown"
        uri = post.get("uri") or ""
        return {
            "id": post.get("cid") or uri,
            "text": text,
            "author": handle,
            "url": bluesky_uri_to_url(uri),
            "like_count": int(post.get("like_count") or 0),
            "repost_count": int(post.get("repost_count") or 0),
        }
    except Exception:
        return None


def normalize_mastodon_post(post: dict) -> dict | None:
    """Extract fields from a raw Mastodon status dict."""
    try:
        text = strip_html(post.get("content") or "").strip()
        if not text:
            return None
        account = post.get("account") or {}
        author = account.get("acct") or account.get("username") or "unknown"
        return {
            "id": str(post.get("id") or ""),
            "text": text,
            "author": author,
            "url": post.get("url") or post.get("uri") or "",
            "like_count": int(post.get("favourites_count") or 0),
            "repost_count": int(post.get("reblogs_count") or 0),
        }
    except Exception:
        return None


PLATFORMS: list[dict] = [
    {
        "name": "bluesky",
        "fetch": bluesky.collect_search_posts,
        "normalize": normalize_bluesky_post,
        "fetch_kwargs": {"sort": "top"},
    },
    {
        "name": "mastodon",
        "fetch": mastodon.collect_search_posts,
        "normalize": normalize_mastodon_post,
        "fetch_kwargs": {},
    },
]


def _clamp_limit(n: int) -> int:
    return max(1, min(MAX_LIMIT_PER_PLATFORM, n))


def analyze_topic(
    topic: str,
    *,
    bluesky_limit: int | None = None,
    mastodon_limit: int | None = None,
    limit: int | None = None,
    top_n: int = 5,
) -> dict:
    """
    Fetch posts for *topic* from every registered platform, score each with
    VADER, and return top_n posts plus unified sentiment percentages.

    Limits: each platform uses its own arg if set, else shared *limit*, else
    defaults (Bluesky 100, Mastodon 25). Values are clamped to 1–500.

    Collectors paginate with a small delay between pages and a page cap per
    platform (see apis.bluesky / apis.mastodon). Partial results may include
    an entry in *errors* when the page cap stops the fetch early.

    Can be called directly by a DB ingestion script — no HTTP layer needed.
    """
    eff_bluesky = bluesky_limit if bluesky_limit is not None else (limit if limit is not None else 100)
    eff_mastodon = mastodon_limit if mastodon_limit is not None else (limit if limit is not None else 25)
    limits_by_name = {
        "bluesky": _clamp_limit(eff_bluesky),
        "mastodon": _clamp_limit(eff_mastodon),
    }

    all_scored: list[dict] = []
    per_platform_counts: dict[str, int] = {}
    errors: dict[str, str] = {}

    for platform in PLATFORMS:
        name: str = platform["name"]
        fetch = platform["fetch"]
        normalize = platform["normalize"]
        fetch_kwargs: dict = platform.get("fetch_kwargs") or {}
        target = limits_by_name[name]

        result = fetch(topic, limit=target, **fetch_kwargs)

        if isinstance(result, tuple) and result[0] is None:
            errors[name] = result[1] or "unknown error"
            per_platform_counts[name] = 0
            continue

        if not isinstance(result, dict):
            errors[name] = "unexpected fetch response"
            per_platform_counts[name] = 0
            continue

        if result.get("warning"):
            errors[name] = result["warning"]

        raw_posts: list[dict] = result.get("posts", [])
        platform_scored: list[dict] = []

        for raw in raw_posts:
            normalized = normalize(raw)
            if normalized is None:
                continue
            sentiment = score_post(normalized["text"])
            platform_scored.append({"platform": name, **normalized, **sentiment})

        per_platform_counts[name] = len(platform_scored)
        all_scored.extend(platform_scored)

    total = len(all_scored)

    counts = {"positive": 0, "neutral": 0, "negative": 0}
    for post in all_scored:
        counts[post["label"]] += 1

    def pct(n: int) -> float:
        return round(n / total * 100, 2) if total else 0.0

    unified = {
        "positive_pct": pct(counts["positive"]),
        "neutral_pct": pct(counts["neutral"]),
        "negative_pct": pct(counts["negative"]),
        "avg_compound": round(sum(p["compound"] for p in all_scored) / total, 4) if total else 0.0
    }

    bluesky_posts = [p for p in all_scored if p["platform"] == "bluesky"]
    top_posts = sorted(bluesky_posts, key=lambda p: p["like_count"] + p["repost_count"], reverse=True)[:top_n]

    result_payload: dict = {
        "topic": topic,
        "total_posts": total,
        "per_platform_counts": per_platform_counts,
        "unified": unified,
        "top_posts": top_posts,
    }
    if errors:
        result_payload["errors"] = errors

    return result_payload
