import pytest

from app import app
from models import db, User


@pytest.fixture
def client():
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        JWT_SECRET_KEY="test-secret-key-for-testing-123456789"
    )

    with app.app_context():
        db.drop_all()
        db.create_all()

    with app.test_client() as client:
        yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()


def signup(client, username, password="password123"):
    return client.post(
        "/signup",
        json={
            "username": username,
            "password": password
        }
    )


def login(client, username, password="password123"):
    response = client.post(
        "/login",
        json={
            "username": username,
            "password": password
        }
    )

    return response.get_json()["access_token"]


def auth_headers(token):
    return {
        "Authorization": f"Bearer {token}"
    }


def test_signup(client):
    response = signup(client, "Tabby")

    assert response.status_code == 201

    data = response.get_json()

    assert data["user"]["username"] == "Tabby"
    assert "password" not in data["user"]


def test_duplicate_signup(client):
    signup(client, "Prince")

    response = signup(client, "Prince")

    assert response.status_code == 409


def test_password_is_hashed(client):
    signup(client, "Zakaria")

    with app.app_context():
        user = User.query.filter_by(username="Zakaria").first()

        assert user.password_hash != "password123"
        assert user.password_hash.startswith("$2b$")


def test_login(client):
    signup(client, "Wesley")

    response = client.post(
        "/login",
        json={
            "username": "Wesley",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Login successful"
    assert "access_token" in data


def test_invalid_login(client):
    signup(client, "Tabby")

    response = client.post(
        "/login",
        json={
            "username": "Tabby",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401


def test_me_requires_authentication(client):
    response = client.get("/me")

    assert response.status_code == 401


def test_me_returns_current_user(client):
    signup(client, "Tabby")

    token = login(client, "Tabby")

    response = client.get(
        "/me",
        headers=auth_headers(token)
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["user"]["username"] == "Tabby"


def test_create_note(client):
    signup(client, "Tabby")

    token = login(client, "Tabby")

    response = client.post(
        "/notes",
        json={
            "title": "Test Note",
            "content": "This is a test note."
        },
        headers=auth_headers(token)
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["note"]["title"] == "Test Note"
    assert data["note"]["content"] == "This is a test note."
    assert data["note"]["user_id"] == 1


def test_notes_require_authentication(client):
    response = client.get("/notes")

    assert response.status_code == 401


def test_get_notes(client):
    signup(client, "Tabby")

    token = login(client, "Tabby")

    client.post(
        "/notes",
        json={
            "title": "First Note",
            "content": "First content"
        },
        headers=auth_headers(token)
    )

    response = client.get(
        "/notes",
        headers=auth_headers(token)
    )

    assert response.status_code == 200

    data = response.get_json()

    assert len(data["notes"]) == 1
    assert data["pagination"]["total"] == 1


def test_update_note(client):
    signup(client, "Tabby")

    token = login(client, "Tabby")

    create_response = client.post(
        "/notes",
        json={
            "title": "Old Title",
            "content": "Old content"
        },
        headers=auth_headers(token)
    )

    note_id = create_response.get_json()["note"]["id"]

    response = client.patch(
        f"/notes/{note_id}",
        json={
            "title": "New Title",
            "content": "New content"
        },
        headers=auth_headers(token)
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["note"]["title"] == "New Title"
    assert data["note"]["content"] == "New content"


def test_delete_note(client):
    signup(client, "Tabby")

    token = login(client, "Tabby")

    create_response = client.post(
        "/notes",
        json={
            "title": "Delete Me",
            "content": "This note will be deleted."
        },
        headers=auth_headers(token)
    )

    note_id = create_response.get_json()["note"]["id"]

    response = client.delete(
        f"/notes/{note_id}",
        headers=auth_headers(token)
    )

    assert response.status_code == 200


def test_user_cannot_access_another_users_note(client):
    signup(client, "Tabby")
    signup(client, "Prince")

    tabby_token = login(client, "Tabby")
    prince_token = login(client, "Prince")

    create_response = client.post(
        "/notes",
        json={
            "title": "Prince Private Note",
            "content": "Private content"
        },
        headers=auth_headers(prince_token)
    )

    note_id = create_response.get_json()["note"]["id"]

    response = client.get(
        f"/notes/{note_id}",
        headers=auth_headers(tabby_token)
    )

    assert response.status_code == 403


def test_pagination(client):
    signup(client, "Tabby")

    token = login(client, "Tabby")

    for number in range(3):
        client.post(
            "/notes",
            json={
                "title": f"Note {number}",
                "content": f"Content {number}"
            },
            headers=auth_headers(token)
        )

    response = client.get(
        "/notes?page=1&per_page=2",
        headers=auth_headers(token)
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["pagination"]["page"] == 1
    assert data["pagination"]["per_page"] == 2
    assert data["pagination"]["total"] == 3
    assert data["pagination"]["pages"] == 2
    assert data["pagination"]["has_next"] is True
