import re

_COMPOUND_POSITIVE_THRESHOLD = 0.05
_COMPOUND_NEGATIVE_THRESHOLD = -0.05


def strip_html(html: str) -> str:
    """Remove HTML tags and decode common entities from a string."""
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&gt;", ">", text)
    text = re.sub(r"&quot;", '"', text)
    text = re.sub(r"&#39;", "'", text)
    text = re.sub(r"&[a-zA-Z]+;", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def sentiment_label(compound: float) -> str:
    """Map a VADER compound score to a human-readable sentiment label."""
    if compound >= _COMPOUND_POSITIVE_THRESHOLD:
        return "positive"
    if compound <= _COMPOUND_NEGATIVE_THRESHOLD:
        return "negative"
    return "neutral"


def strip_urls(text: str) -> str:
    """Remove bare URLs from text so they don't skew VADER scoring."""
    return re.sub(r"https?://\S+", "", text).strip()


def bluesky_uri_to_url(uri: str) -> str:
    """
    Convert a Bluesky at-URI to a bsky.app web URL.

    at://did:.../app.bsky.feed.post/<rkey> → https://bsky.app/profile/<did>/post/<rkey>
    Returns the original uri unchanged if it cannot be converted.
    """
    if not uri.startswith("at://"):
        return uri
    parts = uri.removeprefix("at://").split("/")
    if len(parts) == 3:
        return f"https://bsky.app/profile/{parts[0]}/post/{parts[2]}"
    return uri
