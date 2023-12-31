import pytest

from myapp import create_app_testing, db
from myapp.routes import limiter

@pytest.fixture()
def app():
    app = create_app_testing("sqlite://")
    limiter.enabled = False  # Disable rate limiting

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()