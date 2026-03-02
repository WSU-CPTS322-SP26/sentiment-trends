import config
from atproto import Client


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
    if limit is not None and (limit < 1):
        limit = 25
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
