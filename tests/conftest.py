import pytest

from app import create_app, Config, db
from app.users.models import Role, User


@pytest.fixture()
def app():
    config = Config()
    config.SQLALCHEMY_DATABASE_URI = "sqlite://"
    config.PAGE_SIZE = 5
    config.TESTING = True
    app = create_app(config)

    with app.app_context():
        db.create_all()
        admin_role = Role(name="Admin")
        editor_role = Role(name="Editor")
        viewer_role = Role(name="Viewer")
        db.session.add_all([admin_role, editor_role, viewer_role])
        db.session.commit()
        app.cached_roles = {role.name.lower(): role for role in db.session.query(Role).all()}

    yield app


@pytest.fixture()
def client(app):
    client = app.test_client()
    app.app_context().push()
    return client


@pytest.fixture
def tokens(app, client):
    username = "admin"
    password = "Admin12345"

    with app.app_context():
        user = User(username=username, password=password, role_id=app.cached_roles["admin"].id)
        db.session.add(user)
        db.session.commit()

    login_response = client.post(f"auth/login", json={
        "username": username,
        "password": password
    })
    assert login_response.status_code == 200
    return login_response.json


@pytest.fixture
def access_headers(tokens):
    return {"Authorization": f"Bearer {tokens['access_token']}"}


@pytest.fixture
def refresh_headers(tokens):
    return {"Authorization": f"Bearer {tokens['refresh_token']}"}


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def with_user(app):
    username = "admin1"
    password = "Admin12345"
    with app.app_context():
        user = User(username=username, password=password, role_id=app.cached_roles["admin"].id)
        db.session.add(user)
        db.session.commit()
        yield user.id, username, password
