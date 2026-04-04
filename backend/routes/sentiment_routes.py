from flask import Blueprint, jsonify, request

from services import sentiment

sentiment_bp = Blueprint("sentiment", __name__, url_prefix="/sentiment")

_MAX = sentiment.MAX_LIMIT_PER_PLATFORM


def _parse_optional_positive_int(name: str) -> int | None:
    raw = request.args.get(name, type=int)
    if raw is None:
        return None
    if raw < 1:
        return None
    return min(_MAX, raw)


# GET /sentiment/analyze?topic=elections&limit=25&bluesky_limit=100&mastodon_limit=40&top_n=5
@sentiment_bp.route("/analyze", methods=["GET"])
def analyze():
    topic = request.args.get("topic") or request.args.get("q", "").strip()
    if not topic:
        return jsonify({"error": "topic query parameter is required"}), 400

    limit = request.args.get("limit", default=25, type=int)
    top_n = request.args.get("top_n", default=5, type=int)
    bluesky_limit = _parse_optional_positive_int("bluesky_limit")
    mastodon_limit = _parse_optional_positive_int("mastodon_limit")

    if limit < 1:
        limit = 25
    limit = min(_MAX, limit)

    if top_n < 1:
        top_n = 5

    try:
        result = sentiment.analyze_topic(
            topic,
            limit=limit,
            bluesky_limit=bluesky_limit,
            mastodon_limit=mastodon_limit,
            top_n=top_n,
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
