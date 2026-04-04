import time

import config
from atproto import Client

# Pagination guardrails for analyze_topic collectors (see services.sentiment).
_MAX_PAGES_PER_PLATFORM = 15
_PAGINATION_SLEEP_SEC = 0.5


def _authenticated_client() -> tuple[Client | None, str | None]:
    """returns (client, None) or (None, error_message)."""
    if config.BLUESKY_SESSION_STRING:
        try:
            client = Client()
            client.login(session_string=config.BLUESKY_SESSION_STRING)
            return (client, None)
        except Exception as e:
            return (None, str(e))
    if config.BLUESKY_HANDLE and config.BLUESKY_APP_PASSWORD:
        try:
            client = Client()
            client.login(config.BLUESKY_HANDLE, config.BLUESKY_APP_PASSWORD)
            return (client, None)
        except Exception as e:
            return (None, str(e))
    return (None, "Credentials not set. Set BLUESKY_HANDLE and BLUESKY_APP_PASSWORD (or BLUESKY_SESSION_STRING) in .env")


def _to_dict(obj) -> dict:
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if hasattr(obj, "dict"):
        return obj.dict()
    return dict(obj)


# request: limit (1–100, optional), cursor (optional)
def get_timeline(limit: int | None = 50, cursor: str | None = None) -> dict | tuple[None, str]:
    client, err = _authenticated_client()
    if not client:
        return (None, err or "Auth failed")
    if limit is not None and (limit < 1 or limit > 100):
        limit = 50
    resp = client.get_timeline(algorithm="reverse-chronological", cursor=cursor, limit=limit)
    feed = [_to_dict(f) for f in resp.feed] if getattr(resp, "feed", None) else []
    return {"cursor": getattr(resp, "cursor", None), "feed": feed}


# request: q (search string), limit (1–100, optional), cursor (optional), sort ('latest'|'top'), tag (list of hashtags, no #)
def search_posts(
    q: str,
    *,
    limit: int | None = 25,
    cursor: str | None = None,
    sort: str = "latest",
    tag: list[str] | None = None,
) -> dict | tuple[None, str]:
    if not q or not q.strip():
        return {"posts": [], "cursor": None, "hits_total": None}
    client, err = _authenticated_client()
    if not client:
        return (None, err or "Auth failed")
    if limit is not None:
        if limit < 1:
            limit = 25
        else:
            limit = min(100, limit)
    params = {"q": q.strip(), "limit": limit, "cursor": cursor, "sort": sort}
    if tag:
        params["tag"] = tag
    resp = client.app.bsky.feed.search_posts(params)
    posts = [_to_dict(p) for p in resp.posts] if getattr(resp, "posts", None) else []
    return {
        "posts": posts,
        "cursor": getattr(resp, "cursor", None),
        "hits_total": getattr(resp, "hits_total", None),
    }


def collect_search_posts(
    q: str,
    *,
    limit: int,
    sort: str = "latest",
    tag: list[str] | None = None,
    max_pages: int = _MAX_PAGES_PER_PLATFORM,
    sleep_sec: float = _PAGINATION_SLEEP_SEC,
) -> dict | tuple[None, str]:
    """Fetch up to *limit* posts using app.bsky.feed.searchPosts cursors (max 100 per request)."""
    if not q or not q.strip():
        return {"posts": [], "warning": None}
    if limit < 1:
        return {"posts": [], "warning": None}

    accumulated: list[dict] = []
    cursor: str | None = None
    pages = 0
    warning: str | None = None

    while len(accumulated) < limit and pages < max_pages:
        chunk = min(100, limit - len(accumulated))
        try:
            result = search_posts(q, limit=chunk, cursor=cursor, sort=sort, tag=tag)
        except Exception as e:
            err_msg = str(e)
            if "429" in err_msg or "Too Many Requests" in err_msg:
                return (None, "Rate limited by Bluesky (429)")
            return (None, err_msg)

        if isinstance(result, tuple) and result[0] is None:
            return (None, result[1] or "unknown error")

        if not isinstance(result, dict):
            return (None, "unexpected response from search_posts")

        batch = result.get("posts") or []
        if not batch:
            break

        accumulated.extend(batch)
        cursor = result.get("cursor")
        pages += 1

        if len(accumulated) >= limit:
            break
        if not cursor:
            break

        time.sleep(sleep_sec)

    accumulated = accumulated[:limit]

    if len(accumulated) < limit and pages >= max_pages:
        warning = (
            f"stopped after {max_pages} requests (page cap); got {len(accumulated)} of {limit}"
        )

    return {"posts": accumulated, "warning": warning}
