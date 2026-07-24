import pytest

@pytest.fixture(scope="module")
def admin_token(client):
    response = client.post(
        "/login",
        data={"username": "admin@test.com", "password": "adminpass"}
    )
    return response.json()["access_token"]

@pytest.fixture(scope="module")
def employee_token(client):
    response = client.post(
        "/login",
        data={"username": "employee@test.com", "password": "employeepass"}
    )
    return response.json()["access_token"]


def test_create_asset_unauthorized(client):
    # Missing token entirely
    response = client.post(
        "/assets/",
        json={
            "name": "Laptop",
            "category": "IT Equipments",
            "status": "Available"
        }
    )
    assert response.status_code == 401

def test_create_asset_forbidden_for_employee(client, employee_token):
    # Employee trying to create an asset
    response = client.post(
        "/assets/",
        headers={"Authorization": f"Bearer {employee_token}"},
        json={
            "name": "Laptop",
            "category": "IT Equipments",
            "status": "Available"
        }
    )
    assert response.status_code == 403

def test_create_asset_success_admin(client, admin_token):
    # Admin creating an asset
    response = client.post(
        "/assets/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "name": "Macbook Pro",
            "category": "IT Equipments",
            "status": "Available"
        }
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Macbook Pro"

def test_get_all_assets_pagination(client, admin_token):
    # Create a second asset to test pagination
    client.post(
        "/assets/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "name": "Office Chair",
            "category": "Furniture",
            "status": "Available"
        }
    )
    
    # Test retrieving with limit=1
    response = client.get(
        "/assets/?limit=1",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Macbook Pro"
    
    # Test offset=1
    response = client.get(
        "/assets/?limit=1&offset=1",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Office Chair"

def test_get_all_assets_search(client, admin_token):
    response = client.get(
        "/assets/?search=Office",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Office Chair"
