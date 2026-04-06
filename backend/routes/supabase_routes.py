from flask import Blueprint, jsonify, request

from db.homepage import get_homepage_topics
from db.topic_detail import get_topic_detail_by_id, get_topic_detail_by_name

supabase_bp = Blueprint("supabase", __name__, url_prefix="/supabase")


# GET /supabase/home
# all topics with latest sentiment for homepage cards
@supabase_bp.route("/home", methods=["GET"])
def home():
    try:
        cards = get_homepage_topics()
        return jsonify({"cards": cards})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# GET /supabase/topic?id=<uuid> or ?topic=<name> or ?q=<name>
# one topic row with latest sentiment plus stored top_posts
@supabase_bp.route("/topic", methods=["GET"])
def topic():
    try:
        topic_id = (request.args.get("id") or "").strip()
        name = (request.args.get("topic") or request.args.get("q") or "").strip()
        if topic_id:
            detail = get_topic_detail_by_id(topic_id)
        elif name:
            detail = get_topic_detail_by_name(name)
        else:
            return jsonify({"error": "id or topic query parameter is required"}), 400
        if detail is None:
            return jsonify({"error": "topic not found"}), 404
        return jsonify(detail)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
