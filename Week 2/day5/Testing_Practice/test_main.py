from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_create_user():

    response = client.post(
        "/users",
        json={
            "username":"laiba",
            "email":"laiba@gmail.com",
            "password":"123456"
        }
    )

    assert response.status_code == 200

    assert response.json()["username"] == "laiba"

def test_duplicate_email():

    client.post(
        "/users",
        json={
            "username":"ali",
            "email":"ali@gmail.com",
            "password":"123456"
        }
    )

    response = client.post(
        "/users",
        json={
            "username":"ahmed",
            "email":"ali@gmail.com",
            "password":"abcdef"
        }
    )

    assert response.status_code == 409

    assert response.json()["detail"] == "Email already exists"

def test_protected_route():

    response = client.get("/users/me")

    assert response.status_code == 401