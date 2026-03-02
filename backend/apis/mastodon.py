import config
from mastodon import Mastodon


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
        # verify credentials work
        client.account_verify_credentials()
        return (client, None)
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


# request: limit (1-100, optional), cursor (optional, treated as max_id)
def get_timeline(limit: int | None = 50, cursor: str | None = None) -> dict | tuple[None, str]:
    """fetch home timeline with pagination."""
    client, err = _authenticated_client()
    if not client:
        return (None, err or "Auth failed")
    if limit is not None and (limit < 1 or limit > 100):
        limit = 50
    try:
        # mastodon uses max_id for pagination
        statuses = client.timeline_home(limit=limit, max_id=cursor)
        feed = [_to_dict(s) for s in statuses]
        # get the oldest status id as next cursor
        next_cursor = statuses[-1]["id"] if statuses else None
        return {"cursor": next_cursor, "feed": feed}
    except Exception as e:
        return (None, str(e))


# request: q (search string), limit (1-40, optional), cursor (optional, treated as offset), sort, tag
# note: mastodon api limitations:
# - search_v2 has no limit parameter (limit kept in signature for api compatibility but not passed)
# - search_v2 has no sort parameter (sort kept in signature for api compatibility but not passed)
# - search_v2 has no tag filter parameter (tag kept in signature for api compatibility but not passed)
# - pagination uses numeric offset instead of cursor tokens
def search_posts(
    q: str,
    *,
    limit: int | None = 25,
    cursor: str | None = None,
    sort: str = "latest",
    tag: list[str] | None = None,
) -> dict | tuple[None, str]:
    """search for posts containing query string."""
    if not q or not q.strip():
        return {"posts": [], "cursor": None, "hits_total": None}
    client, err = _authenticated_client()
    if not client:
        return (None, err or "Auth failed")
    try:
        # convert cursor to offset (mastodon uses numeric offset)
        offset = int(cursor) if cursor else 0
        # mastodon search_v2 only supports: q, result_type, offset, min_id, max_id, account_id, exclude_unreviewed
        # limit, sort, and tag parameters are not supported by the api
        results = client.search_v2(q.strip(), result_type="statuses", offset=offset)
        posts = [_to_dict(s) for s in results.get("statuses", [])]
        # calculate next cursor as offset + limit
        next_cursor = str(offset + len(posts)) if posts else None
        return {
            "posts": posts,
            "cursor": next_cursor,
            "hits_total": len(posts),
        }
    except Exception as e:
        return (None, str(e))
