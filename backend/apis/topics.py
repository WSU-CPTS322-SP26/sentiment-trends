import config
import serpapi


def _topic_row(item: dict) -> dict:
    return {
        "query": item.get("query"),
        "search_volume": item.get("search_volume"),
        "increase_percentage": item.get("increase_percentage"),
        "active": item.get("active"),
        "categories": item.get("categories"),
    }

# returns int for order of popularity of a topic
def _search_volume_sort_key(row: dict) -> int:
    v = row.get("search_volume")
    # if volume is a bool or non numeric put it at the bottom
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return -1
    return int(v)

# hours default to 24, everything else to null.
def get_trending_now(
    *,
    geo: str = "US",
    hours: int | None = None,
    category_id: int | None = None,
    hl: str | None = None,
    only_active: bool | None = None,
    max: int | None = None,
) -> dict | tuple[None, str]:
    # stable "topics" list plus full serpapi json under "raw". if hours is none, serpapi defaults to past 24 hours.
    # if max is set, return the top max topics by search_volume; raw is still the full SerpAPI payload.
    if not config.SERPAPI_KEY:
        return (None, "Credentials not set. Set SERPAPI_KEY in .env")

    params: dict = {
        "engine": "google_trends_trending_now",
        "geo": geo or "US",
    }
    if hours is not None:
        params["hours"] = hours
    if category_id is not None:
        params["category_id"] = category_id
    if hl is not None:
        params["hl"] = hl
    if only_active is not None:
        params["only_active"] = "true" if only_active else "false"

    try:
        client = serpapi.Client(api_key=config.SERPAPI_KEY)
        result = client.search(**params)
    except Exception as e:
        return (None, str(e))

    if not hasattr(result, "get"):
        return (None, "unexpected response from serpapi")

    err = result.get("error")
    if err:
        return (None, str(err))

    meta = result.get("search_metadata") or {}
    if meta.get("status") == "Error":
        return (None, str(result.get("error") or "serpapi search failed"))

    rows = result.get("trending_searches") or []
    topics = [_topic_row(row) for row in rows if isinstance(row, dict)]
    if max is not None:
        topics = sorted(topics, key=_search_volume_sort_key, reverse=True)[:max]
    payload = result.as_dict() if hasattr(result, "as_dict") else dict(result)

    return {"topics": topics, "raw": payload}
