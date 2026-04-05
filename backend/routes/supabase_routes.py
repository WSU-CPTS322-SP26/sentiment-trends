from flask import Blueprint, jsonify

from db.homepage import get_homepage_topics

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
