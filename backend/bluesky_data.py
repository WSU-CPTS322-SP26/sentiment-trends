from backend.apis import bluesky, mastodon
from utils.helpers import bluesky_uri_to_url, sentiment_label, strip_html, strip_urls
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer  # type: ignore[import-untyped]

sia = SentimentIntensityAnalyzer()


# --------------------------
# Helper functions
# --------------------------
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


# --------------------------
# Platform configuration
# --------------------------
PLATFORMS: list[dict] = [
    {
        "name": "bluesky",
        "fetch": bluesky.search_posts,
        "normalize": normalize_bluesky_post,
        "fetch_kwargs": {"sort": "top"},  # optional sorting
    },
    {
        "name": "mastodon",
        "fetch": mastodon.search_posts,
        "normalize": normalize_mastodon_post,
        "fetch_kwargs": {},
    },
]


# --------------------------
# Main analysis function
# --------------------------
def analyze_topic(
    topic: str,
    limit_per_platform: int = 25,
    top_n: int = 5,
) -> dict:
    """
    Fetch posts for *topic* from all platforms, score with VADER, and return:
    - top posts (Bluesky only)
    - unified sentiment percentages
    - total posts per platform
    - errors (if any)
    """
    all_scored: list[dict] = []
    per_platform_counts: dict[str, int] = {}
    errors: dict[str, str] = {}

    for platform in PLATFORMS:
        name = platform["name"]
        fetch = platform["fetch"]
        normalize = platform["normalize"]
        fetch_kwargs = platform.get("fetch_kwargs") or {}

        result = fetch(topic, limit=limit_per_platform, **fetch_kwargs)

        if isinstance(result, tuple) and result[0] is None:
            errors[name] = result[1] or "unknown error"
            per_platform_counts[name] = 0
            continue

        raw_posts: list[dict] = result.get("posts", []) if isinstance(result, dict) else []
        platform_scored: list[dict] = []

        for raw in raw_posts:
            normalized = normalize(raw)
            if not normalized:
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
    }

    # Top posts only from Bluesky
    bluesky_posts = [p for p in all_scored if p["platform"] == "bluesky"]
    top_posts = sorted(
        bluesky_posts,
        key=lambda p: p["like_count"] + p["repost_count"],
        reverse=True
    )[:top_n]

    payload = {
        "topic": topic,
        "total_posts": total,
        "per_platform_counts": per_platform_counts,
        "unified": unified,
        "top_posts": top_posts,
    }
    if errors:
        payload["errors"] = errors

    return payload