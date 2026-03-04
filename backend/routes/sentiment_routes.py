from flask import Blueprint, jsonify, request

from services import sentiment

sentiment_bp = Blueprint("sentiment", __name__, url_prefix="/sentiment")


# GET /sentiment/analyze?topic=elections&limit=25&top_n=5
@sentiment_bp.route("/analyze", methods=["GET"])
def analyze():
    topic = request.args.get("topic") or request.args.get("q", "").strip()
    if not topic:
        return jsonify({"error": "topic query parameter is required"}), 400

    limit = request.args.get("limit", default=25, type=int)
    top_n = request.args.get("top_n", default=5, type=int)

    if limit < 1:
        limit = 25
    if top_n < 1:
        top_n = 5

    try:
        result = sentiment.analyze_topic(topic, limit_per_platform=limit, top_n=top_n)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
