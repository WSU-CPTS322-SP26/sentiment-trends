# shared fixtures for backend tests; no real env or external calls.
import pytest

from app import app as flask_app


@pytest.fixture
def app():
    """return the Flask application instance."""
    return flask_app


@pytest.fixture
def client(app):
    """return test client for the Flask app."""
    return app.test_client()
