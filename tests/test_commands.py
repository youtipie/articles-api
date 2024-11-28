import pytest

from app import db
from app.article.models import Article
from app.commands.routes import create_user, prepopulate_db
from app.users.models import User, Role


@pytest.mark.parametrize("user_data", [
    {"username": "Admin", "password": "Admin12345", "role": "admin"},
    {"username": "Editor", "password": "Editor12345", "role": "editor"},
    {"username": "Viewer", "password": "Viewer12345", "role": "viewer"}
])
def test_create_user(app, runner, user_data):
    username = user_data["username"]
    password = user_data["password"]
    role = user_data["role"]
    with app.app_context():
        result = runner.invoke(create_user, ["--username", username, "--password", password, "--role", role])
        assert result.exit_code == 0
        assert result.output == f"User '{username}' created successfully!\n"
        user = User.query.first()
        assert user.username == username
        assert user.role_id == app.cached_roles[role].id


def test_create_user_invalid_role(app, runner):
    username = "Temp"
    password = "Temp"
    role = "Invalid role"
    with app.app_context():
        result = runner.invoke(create_user, ["--username", username, "--password", password, "--role", role])
        assert result.exit_code == 0
        assert result.output == "Such role does not exist\n"


def test_create_user_invalid_password(app, runner):
    username = "Temp"
    password = "Temp"
    role = "admin"
    with app.app_context():
        result = runner.invoke(create_user, ["--username", username, "--password", password, "--role", role])
        assert result.exit_code == 0
        assert result.output == ("Password have to be minimal 8 characters lengths, "
                                 "contain at least one lowercase and uppercase symbol\n")


def test_create_user_invalid_username(app, runner):
    username = "admin"
    password = "Temp12345"
    role = "admin"

    with app.app_context():
        user = User(username=username, password=password, role_id=app.cached_roles["admin"].id)
        db.session.add(user)
        db.session.commit()

        result = runner.invoke(create_user, ["--username", username, "--password", password, "--role", role])
        assert result.exit_code == 0
        assert result.output == "User with such username already exists\n"


def test_prepopulate_db(app, runner):
    with app.app_context():
        result = runner.invoke(prepopulate_db)
        assert result.exit_code == 0
        assert result.output == f"Database has been populated with sample data.\n"
        assert User.query.count() == 3
        assert Role.query.count() == 3
        assert Article.query.count() == 2
