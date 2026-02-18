from flask import Blueprint, jsonify, request

from apis import mastodon

mastodon_bp = Blueprint("mastodon", __name__, url_prefix="/mastodon")


def _error_response(result) -> tuple | None:
    """If result is (None, error_message), return (jsonify({"error": msg}), 401); else None."""
    if isinstance(result, tuple) and len(result) == 2 and result[0] is None:
        return jsonify({"error": result[1]}), 401
    return None

# home timeline requires authenticated account
# request: GET mastodon/timeline?limit=50&cursor=...
# example: http://localhost:3001/mastodon/timeline?limit=50
@mastodon_bp.route("/timeline", methods=["GET"])
def timeline():
    try:
        limit = request.args.get("limit", type=int)
        cursor = request.args.get("cursor")
        result = mastodon.get_timeline(limit=limit, cursor=cursor)
        err_resp = _error_response(result)
        if err_resp is not None:
            return err_resp
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 401


# request: GET mastodon/search?topic=... or q=...
# example: http://localhost:3001/mastodon/search?topic=elections or http://localhost:3001/mastodon/search?q=elections
@mastodon_bp.route("/search", methods=["GET"])
def search():
    try:
        topic = request.args.get("topic") or request.args.get("q", "")
        limit = request.args.get("limit", type=int)
        cursor = request.args.get("cursor")
        sort = request.args.get("sort", "latest")
        raw_tags = request.args.get("tag", "")
        tag = [t.strip() for t in raw_tags.split(",") if t.strip()] if raw_tags else None
        result = mastodon.search_posts(topic, limit=limit, cursor=cursor, sort=sort, tag=tag)
        err_resp = _error_response(result)
        if err_resp is not None:
            return err_resp
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 401
