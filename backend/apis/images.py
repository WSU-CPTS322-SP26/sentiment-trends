import config
import serpapi

_MAX_IMAGES = 10


# returns direct image url from one row (original, else link), or none if unusable
def _image_url(row: dict) -> str | None:
    u = row.get("original") or row.get("link")
    if isinstance(u, str) and u.strip():
        return u.strip()
    return None


# count defaults to 3, capped at _MAX_IMAGES.
def get_topic_images(topic: str, *, count: int = 3) -> dict | tuple[None, str]:
    # stable "images" list of url strings plus full serpapi json under "raw".
    # rows without original/link are skipped until count urls are collected or results run out.
    if not config.SERPAPI_KEY:
        return (None, "Credentials not set. Set SERPAPI_KEY in .env")

    q = (topic or "").strip()
    if not q:
        return (None, "topic must be a non-empty string")

    if not isinstance(count, int) or count < 1:
        return (None, "count must be an integer >= 1")
    n = min(count, _MAX_IMAGES)

    try:
        client = serpapi.Client(api_key=config.SERPAPI_KEY)
        result = client.search(engine="google_images", q=q)
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

    rows = result.get("images_results") or []
    images: list[str] = []
    for row in rows:
        if len(images) >= n:
            break
        if not isinstance(row, dict):
            continue
        u = _image_url(row)
        if u:
            images.append(u)
    payload = result.as_dict() if hasattr(result, "as_dict") else dict(result)

    return {"images": images, "raw": payload}
