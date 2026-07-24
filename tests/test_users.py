def test_register_user(client):
    response = client.post(
        "/users/",
        json={
            "firstname": "Test",
            "lastname": "User",
            "email": "newuser@test.com",
            "password": "password123",
            "role": "employee"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@test.com"
    assert "id" in data

def test_register_existing_user(client):
    response = client.post(
        "/users/",
        json={
            "firstname": "Admin",
            "lastname": "User",
            "email": "admin@test.com", # This email is already seeded by conftest
            "password": "password123",
            "role": "admin"
        }
    )
    assert response.status_code == 400

def test_login_success(client):
    response = client.post(
        "/login",
        data={
            "username": "admin@test.com",
            "password": "adminpass"
        }
    )
    assert response.status_code == 201 # Your login route returns 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"

def test_login_fail(client):
    response = client.post(
        "/login",
        data={
            "username": "admin@test.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
