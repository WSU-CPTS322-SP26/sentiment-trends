import config
from flask import Flask, jsonify
from flask_cors import CORS

from routes import register_blueprints

app = Flask(__name__)
CORS(app)
register_blueprints(app)


@app.route("/")
def index():
    return jsonify({"message": "Backend is running"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3001)
