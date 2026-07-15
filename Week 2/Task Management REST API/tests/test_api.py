
# Test 1 register user
def test_register(client):

    response = client.post(
        "/auth/register",
        json={
            "username": "laiba",
            "email": "laiba@test.com",
            "password": "123456"
        }
    )

    assert response.status_code == 201

# Test_2 login
def test_login(client):

    response = client.post(
        "/auth/login",
        data={
            "username": "laiba@test.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200

    assert "access_token" in response.json()


# Test_3 Create Task

def test_create_task(client):

    login = client.post(
        "/auth/login",
        data={
            "username": "laiba@test.com",
            "password": "123456"
        }
    )

    token = login.json()["access_token"]


    response = client.post(
        "/tasks/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Pytest Task",
            "description": "Testing",
            "status": "pending",
            "due_date": "2026-07-20"
        }
    )

    assert response.status_code == 201

# Test_4 Get Tasks

def test_get_tasks(client):

    login = client.post(
        "/auth/login",
        data={
            "username": "laiba@test.com",
            "password": "123456"
        }
    )

    token = login.json()["access_token"]


    response = client.get(
        "/tasks/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

# Test 5  Unauthorized

def test_unauthorized(client):

    response = client.get("/tasks/")

    assert response.status_code == 401

