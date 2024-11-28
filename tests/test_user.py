import random
from unittest.mock import patch

import pytest

from app import db
from app.users.models import User, Role

USERS_AMOUNT = 10


@pytest.fixture
def generate_users(app):
    with app.app_context():
        for i in range(USERS_AMOUNT):
            username = f"user{i}"
            password = f"UserPassword{i}"
            role_id = random.choice(Role.query.all()).id

            user = User(username=username, password=password, role_id=role_id)
            db.session.add(user)
        db.session.commit()


def test_get_roles(client):
    response = client.get("/users/roles")
    assert response.status_code == 200
    assert len(response.json) == 3


def test_login(client, with_user):
    _, username, password = with_user

    response = client.post("/auth/login", json={"username": username, "password": password})
    assert response.status_code == 200
    assert response.json["access_token"] is not None
    assert response.json["refresh_token"] is not None


def test_login_invalid_data(client):
    response = client.post("/auth/login", json={"username": "username", "password": "password"})
    assert response.status_code == 401
    assert "Invalid username or password" in response.json["message"]


def test_login_empty_body(client):
    response = client.post("/auth/login", json={})
    assert response.status_code == 400
    assert "Request body must be JSON and contain" in response.json["message"]


def test_refresh_token(client, refresh_headers):
    response = client.post("/auth/refresh", headers=refresh_headers)
    assert response.status_code == 200
    assert response.json["access_token"] is not None


def test_get_all_users(app, client, access_headers, generate_users):
    response = client.get("/users", headers=access_headers)
    data = response.json
    assert response.status_code == 200
    assert data["has_prev"] == False
    assert data["has_next"] == True
    assert data["page"] == 1
    assert data["pages"] == 3
    assert len(data["result"]) == app.config["PAGE_SIZE"]
    assert data["total"] == USERS_AMOUNT + 1


def test_get_all_users_using_page(app, client, access_headers, generate_users):
    response = client.get("/users?page=2", headers=access_headers)
    data = response.json
    assert response.status_code == 200
    assert data["has_prev"] == True
    assert data["has_next"] == True
    assert data["page"] == 2
    assert data["pages"] == 3
    assert len(data["result"]) == app.config["PAGE_SIZE"]
    assert data["total"] == USERS_AMOUNT + 1


def test_get_all_users_invalid_page(client, access_headers):
    response = client.get("/users?page=invalid", headers=access_headers)
    assert response.status_code == 400
    assert response.json["message"] == "Page number must be int value"


def test_get_user_by_username(client, access_headers):
    # SQLite does not support FTS with match, have to mock it
    with patch("sqlalchemy.orm.attributes.InstrumentedAttribute.match") as mock_match:
        mock_match.return_value = User.username.like("%admin%")
        response = client.get("/users?username=admin", headers=access_headers)
        data = response.json
        user = data["result"][0]
        assert response.status_code == 200
        assert data["has_prev"] == False
        assert data["has_next"] == False
        assert data["page"] == 1
        assert data["pages"] == 1
        assert len(data["result"]) == 1
        assert data["total"] == 1
        assert user["username"] == "admin"


def test_get_user_by_id(client, access_headers):
    response = client.get("/users?id=1", headers=access_headers)
    user = response.json
    assert response.status_code == 200
    assert user["username"] == "admin"


def test_update_user(app, client, access_headers, generate_users):
    with app.app_context():
        user_to_update = User.query.filter_by(id=2).first()
        old_role = user_to_update.role

    new_username = "Updated username"
    new_password = "NewSecurePassword12345"
    new_role = random.choice([role for role in app.cached_roles.keys() if role != old_role.name])

    response = client.put("/users", headers=access_headers, json={
        "user_id": user_to_update.id,
        "username": new_username,
        "password": new_password,
        "role": new_role
    })
    data = response.json
    assert response.status_code == 200
    assert data["message"] == "Changed user successfully"

    with app.app_context():
        user = User.query.filter_by(id=user_to_update.id).first()
        assert user.username == new_username
        assert user.role_id == app.cached_roles[new_role].id
        assert user.password != user_to_update.password


def test_delete_user(app, client, access_headers, generate_users):
    response = client.delete("/users", headers=access_headers, json={"user_id": 2})
    assert response.status_code == 200
    assert response.json["message"] == "User deleted successfully"
    with app.app_context():
        user = User.query.filter_by(id=2).first()
        assert user is None
