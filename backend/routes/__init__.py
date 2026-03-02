from flask import Flask

from routes.bluesky_routes import bluesky_bp
from routes.mastodon_routes import mastodon_bp


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(bluesky_bp)
    app.register_blueprint(mastodon_bp)
