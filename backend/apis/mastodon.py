import time

import requests

import config
from mastodon import Mastodon
from mastodon.errors import MastodonRatelimitError

_MAX_PAGES_PER_PLATFORM = 15
_PAGINATION_SLEEP_SEC = 0.5


def _authenticated_client() -> tuple[Mastodon | None, str | None]:
    """returns (client, None) or (None, error_message)."""
    if not config.MASTODON_ACCESS_TOKEN:
        return (None, "Credentials not set. Set MASTODON_CLIENT_KEY, MASTODON_CLIENT_SECRET, and MASTODON_ACCESS_TOKEN in .env")
    try:
        client = Mastodon(
            client_id=config.MASTODON_CLIENT_KEY,
            client_secret=config.MASTODON_CLIENT_SECRET,
            access_token=config.MASTODON_ACCESS_TOKEN,
            api_base_url=config.MASTODON_INSTANCE_URL
        )
        client.account_verify_credentials()
        return (client, None)
    except MastodonRatelimitError as e:
        return (None, f"Mastodon rate limit: {e}")
    except Exception as e:
        return (None, str(e))


def _to_dict(obj) -> dict:
    """convert mastodon object to dict."""
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if hasattr(obj, "dict"):
        return obj.dict()
    return dict(obj)


def _v2_search_statuses_page(q: str, offset: int, page_limit: int) -> dict | tuple[None, str]:
    """One GET /api/v2/search with type=statuses; page_limit clamped 1–40 (Mastodon API max)."""
    if not config.MASTODON_ACCESS_TOKEN:
        return (None, "Credentials not set. Set MASTODON_CLIENT_KEY, MASTODON_CLIENT_SECRET, and MASTODON_ACCESS_TOKEN in .env")
    base = (config.MASTODON_INSTANCE_URL or "").rstrip("/")
    if not base:
        return (None, "MASTODON_INSTANCE_URL is not set")
    pl = max(1, min(40, page_limit))
    off = max(0, offset)
    try:
        r = requests.get(
            f"{base}/api/v2/search",
            params={"q": q.strip(), "type": "statuses", "offset": off, "limit": pl},
            headers={"Authorization": f"Bearer {config.MASTODON_ACCESS_TOKEN}"},
            timeout=60,
        )
        if r.status_code == 429:
            return (None, "Rate limited by Mastodon instance (HTTP 429)")
        if not r.ok:
            return (None, r.text or f"HTTP {r.status_code}")
        data = r.json()
        statuses = data.get("statuses") or []
        posts = [_to_dict(s) for s in statuses]
        next_cursor = str(off + len(posts)) if posts else None
        return {"posts": posts, "cursor": next_cursor, "hits_total": None}
    except requests.RequestException as e:
        return (None, str(e))


# request: limit (1-100, optional), cursor (optional, treated as max_id)
def get_timeline(limit: int | None = 50, cursor: str | None = None) -> dict | tuple[None, str]:
    """fetch home timeline with pagination."""
    client, err = _authenticated_client()
    if not client:
        return (None, err or "Auth failed")
    if limit is not None and (limit < 1 or limit > 100):
        limit = 50
    try:
        statuses = client.timeline_home(limit=limit, max_id=cursor)
        feed = [_to_dict(s) for s in statuses]
        next_cursor = statuses[-1]["id"] if statuses else None
        return {"cursor": next_cursor, "feed": feed}
    except Exception as e:
        return (None, str(e))


# Single page: limit 1–40 for the request. sort/tag are accepted for API compatibility but not sent (search_v2 has no sort/tag).
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
    offset = int(cursor) if cursor else 0
    req_limit = 25 if limit is None else max(1, min(40, limit))
    return _v2_search_statuses_page(q.strip(), offset, req_limit)


def collect_search_posts(
    q: str,
    *,
    limit: int,
    max_pages: int = _MAX_PAGES_PER_PLATFORM,
    sleep_sec: float = _PAGINATION_SLEEP_SEC,
) -> dict | tuple[None, str]:
    """Fetch up to *limit* statuses via /api/v2/search offset pagination (max 40 per request)."""
    if not q or not q.strip():
        return {"posts": [], "warning": None}
    if limit < 1:
        return {"posts": [], "warning": None}

    client, err = _authenticated_client()
    if not client:
        return (None, err or "Auth failed")

    accumulated: list[dict] = []
    offset = 0
    pages = 0
    warning: str | None = None

    while len(accumulated) < limit and pages < max_pages:
        chunk = min(40, limit - len(accumulated))
        res = _v2_search_statuses_page(q.strip(), offset, chunk)
        if isinstance(res, tuple) and res[0] is None:
            return (None, res[1] or "unknown error")
        if not isinstance(res, dict):
            return (None, "unexpected response from search")

        batch = res.get("posts") or []
        if not batch:
            break

        accumulated.extend(batch)
        offset += len(batch)
        pages += 1

        if len(accumulated) >= limit:
            break

        time.sleep(sleep_sec)

    accumulated = accumulated[:limit]

    if len(accumulated) < limit and pages >= max_pages:
        warning = (
            f"stopped after {max_pages} requests (page cap); got {len(accumulated)} of {limit}"
        )

    return {"posts": accumulated, "warning": warning}
