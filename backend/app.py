from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"message": "Backend is running"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3001)
