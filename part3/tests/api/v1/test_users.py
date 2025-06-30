import pytest
import uuid


def test_create_user(client):
    """Test the creation of a user"""
    unique_email = f"jane.doe{uuid.uuid4().hex[:6]}@example.com"
    response = client.post('/api/v1/users/', json={
        "first_name": "Jane",
        "last_name": "Doe",
        "email": unique_email,
        "password": "12345678"
    })
    assert response.status_code == 201
    data = response.get_json()
    user_id = data["id"]
    assert "id" in data
    response = client.get(f'/api/v1/users/{user_id}')
    data = response.get_json()
    assert data["first_name"] == "Jane"
    assert data["last_name"] == "Doe"
    assert data["email"] == unique_email
    assert "password" not in data  # Assert 'password' is not in the response


def test_create_user_fail_missing_data(client):
    """Test creating a user with missing data"""
    response = client.post('/api/v1/users/', json={
        "first_name": "Jane",
        "last_name": "Doe",
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "errors" in data
    assert "email" in data["errors"]
    assert data["errors"]["email"] == "'email' is a required property"
    assert data["message"] == "Input payload validation failed"


def test_create_user_fail_missing_data(client):
    """Test creating a user with missing data"""
    response = client.post('/api/v1/users/', json={
        "first_name": "Jane",
        "email": f"jane.doe{uuid.uuid4().hex[:6]}@example.com",
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "errors" in data
    assert "last_name" in data["errors"]
    assert data["errors"]["last_name"] == "'last_name' is a required property"
    assert data["message"] == "Input payload validation failed"


def test_create_user_fail_invalid_data(client):
    """Test creating a user with invalid email"""
    response = client.post('/api/v1/users/', json={
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "invalid-email",
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "errors" in data
    assert "email" in data["errors"]
    assert data["message"] == "Input payload validation failed"


def test_create_user_fail_duplicate_email(client, create_user):
    """Test creating a user with a duplicate email"""
    email = f"john.doe{uuid.uuid4().hex[:6]}@example.com"
    create_user("John", "Doe", email)

    response = client.post('/api/v1/users/', json={
        "first_name": "Davis",
        "last_name": "Daniels",
        "email": email,
        "password": "12345678"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Email already registered"


def test_get_all_users(client, create_user):
    """Test retrieving all users"""
    unique_email = f"alice{uuid.uuid4().hex[:6]}@example.com"
    user1_id = create_user("Alice", "Smith", unique_email)

    response = client.get('/api/v1/users/')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    # Filter the response data to find the user with the unique email
    alice = next((user for user in data if user["email"] == unique_email), None)

    assert alice is not None
    assert "password" not in alice  # Assert 'password' is not in the response
    assert alice["first_name"] == "Alice"
    assert alice["last_name"] == "Smith"
    assert alice["email"] == unique_email
    assert alice["is_admin"] == False
    assert "created_at" in alice
    assert "updated_at" in alice


def test_get_user_by_id(client, create_user):
    """Test retrieving a specific user by ID"""
    unique_email = f"betty{uuid.uuid4().hex[:6]}@example.com"
    user_id = create_user("Betty", "Smith", unique_email)
    response = client.get(f'/api/v1/users/{user_id}')
    user = response.get_json()
    assert response.status_code == 200
    assert user["first_name"] == "Betty"
    assert user["last_name"] == "Smith"
    assert user["email"] == unique_email


def test_get_user_not_found(client):
    """Test retrieving a non-existent user"""
    response = client.get('/api/v1/users/99999')
    assert response.status_code == 404


def test_update_user(client, create_user, auth_header):
    """Test updating an existing user"""
    unique_email = f"bob{uuid.uuid4().hex[:6]}@example.com"
    user_id = create_user("Bob", "Brown", unique_email)
    headers = auth_header(unique_email)

    response = client.put(f'/api/v1/users/{user_id}', json={
        "first_name": "Robert",
        "last_name": "Brown",
    }, headers=headers)
    assert response.status_code == 200
    assert response.get_json()["first_name"] == "Robert"


def test_update_user_unauthorized(client, create_user, auth_header):
    # we try to forge a jwt from other user just
    # to try a non existing user update
    user_email = f"bobbob{uuid.uuid4().hex[:6]}@example.com"
    user_id = create_user("Bob", "Brown", user_email)
    unauthorized_user_email = f"unauth_orized{uuid.uuid4().hex[:6]}@example.com"
    unauthorized_user_id = create_user(
        "Unauth", "Orized", unauthorized_user_email)
    unauthorized_headers = auth_header(unauthorized_user_email)
    """Test updating a non-existent user"""
    response = client.put(f'/api/v1/users/{user_id}', json={
        "first_name": "Unknown",
        "last_name": "User",
        "email": user_email,
    }, headers=unauthorized_headers)
    assert response.status_code == 400


def test_delete_user(client, create_user):
    """Test deleting an existing user"""
    unique_email = f"charlie{uuid.uuid4().hex[:6]}@example.com"
    user_id = create_user("Charlie", "Chaplin", unique_email)

    response = client.delete(f'/api/v1/users/{user_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "User deleted successfully"

    response = client.get(f'/api/v1/users/{user_id}')
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "User not found"
