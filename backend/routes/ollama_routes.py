from flask import Blueprint, jsonify, request

from services.sentiment import MAX_LIMIT_PER_PLATFORM, analyze_topic
from services.summary import summarize_topic

ollama_bp = Blueprint("ollama", __name__, url_prefix="/ollama")


def _parse_limit() -> int:
    limit = request.args.get("limit", default=25, type=int)
    if limit < 1:
        limit = 25
    return min(MAX_LIMIT_PER_PLATFORM, limit)


@ollama_bp.route("/summary", methods=["GET"])
def summary():
    topic = request.args.get("topic") or request.args.get("q", "").strip()
    if not topic:
        return jsonify({"error": "topic query parameter is required"}), 400

    limit = _parse_limit()
    top_n = request.args.get("top_n", default=5, type=int)
    if top_n < 1:
        top_n = 5

    try:
        analysis = analyze_topic(topic, limit=limit, top_n=top_n)
        posts = analysis.get("top_posts") or []
        summary_text = summarize_topic(topic, posts)

        if summary_text is None:
            return jsonify({"error": "Summary unavailable"}), 503

        return jsonify(
            {
                "topic": topic,
                "summary": summary_text,
                "source_post_count": len(posts),
                "analysis_errors": analysis.get("errors") or {},
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500