import config
import serpapi


def _to_bucket_ts(raw: object) -> int | None:
    """Coerce SerpAPI timestamp (seconds or ms) to int for bigint storage."""
    if raw is None:
        return None
    if isinstance(raw, bool):
        return None
    if isinstance(raw, int):
        return raw
    if isinstance(raw, float):
        return int(raw)
    if isinstance(raw, str):
        s = raw.strip()
        if not s:
            return None
        try:
            return int(float(s))
        except ValueError:
            return None
    return None


def _extract_timeline_value(row: dict) -> int | None:
    """First series extracted_value from a timeline_data row, if present."""
    vals = row.get("values")
    if not isinstance(vals, list) or not vals:
        return None
    v0 = vals[0]
    if not isinstance(v0, dict):
        return None
    ev = v0.get("extracted_value")
    if ev is None:
        return None
    if isinstance(ev, bool):
        return None
    if isinstance(ev, int):
        return ev
    if isinstance(ev, float):
        return int(ev)
    if isinstance(ev, str):
        s = ev.strip()
        if not s:
            return None
        try:
            return int(float(s))
        except ValueError:
            return None
    return None


def _timeline_row(row: dict, query: str) -> dict | None:
    """Map one SerpAPI timeline_data dict to DB-ready fields (without topic_id/geo/fetched_at)."""
    ts = _to_bucket_ts(row.get("timestamp"))
    if ts is None:
        return None
    val = _extract_timeline_value(row)
    if val is None:
        return None
    label_raw = row.get("date")
    bucket_label = label_raw.strip() if isinstance(label_raw, str) and label_raw.strip() else None
    return {
        "bucket_ts": ts,
        "bucket_label": bucket_label,
        "value": val,
        "query": query,
    }


def get_interest_over_time(
    query: str,
    *,
    geo: str = "US",
    date: str | None = None,
    hl: str | None = None,
) -> dict | tuple[None, str]:
    """Fetch Google Trends interest-over-time via SerpAPI.

    Returns:
        ``{"timeline": [...], "raw": payload}`` on success, or ``(None, error_message)``.
        Each timeline item has ``bucket_ts``, ``bucket_label``, ``value``, ``query``.
    """
    if not config.SERPAPI_KEY:
        return (None, "Credentials not set. Set SERPAPI_KEY in .env")

    q = (query or "").strip()
    if not q:
        return (None, "query must be a non-empty string")

    params: dict = {
        "engine": "google_trends_interest_over_time",
        "q": q,
        "geo": (geo or "US").strip() or "US",
    }
    if date is not None:
        params["date"] = date
    if hl is not None:
        params["hl"] = hl

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

    iot = result.get("interest_over_time")
    if not isinstance(iot, dict):
        iot = {}

    rows = iot.get("timeline_data") or result.get("timeline_data") or []
    timeline: list[dict] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        mapped = _timeline_row(row, q)
        if mapped:
            timeline.append(mapped)

    payload = result.as_dict() if hasattr(result, "as_dict") else dict(result)

    return {"timeline": timeline, "raw": payload}
