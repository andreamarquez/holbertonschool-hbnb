import pytest
from app import create_app


@pytest.fixture
def app():
    """Initialize the Flask application in test mode"""
    app = create_app(config_name="testing")
    return app


@pytest.fixture
def client(app):
    """Create a test client for the Flask application"""
    return app.test_client()


@pytest.fixture
def create_user(client):
    """Helper function to create a user"""
    def _create_user(first_name, last_name, email, password='12345678'):
        response = client.post('/api/v1/users/', json={
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password
        })
        return (
            response.get_json().get('id')
            if response.status_code == 201
            else None
        )
    return _create_user


def test_create_user(client):
    """Test the creation of a user"""
    response = client.post('/api/v1/users/', json={
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "password": "12345678"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["first_name"] == "Jane"
    assert data["last_name"] == "Doe"
    assert data["email"] == "jane.doe@example.com"


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
        "email": "jane.doe@example.com",
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
    email = "john.doe@example.com"
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
    user1_id = create_user("Alice", "Smith", "alice@example.com")

    response = client.get('/api/v1/users/')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    # Filter the response data to find the user "Alice"
    alice = next(
        (
            user for user in data
            if user["first_name"] == "Alice" and user["last_name"] == "Smith"
        ),
        None
    )

    # Expected data for Alice
    expected_alice = {
        "id": user1_id,
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@example.com",
        "is_admin": False,
        # Use the actual timestamp from the response
        "created_at": alice["created_at"],
        # Use the actual timestamp from the response
        "updated_at": alice["updated_at"],
        "password": alice["password"]
    }

    assert alice is not None
    assert alice == expected_alice


def test_get_user_by_id(client, create_user):
    """Test retrieving a specific user by ID"""
    user_id = create_user("Betty", "Smith", "betty@example.com")
    response = client.get(f'/api/v1/users/{user_id}')
    assert response.status_code == 200
    assert response.get_json()["email"] == "betty@example.com"


def test_get_user_not_found(client):
    """Test retrieving a non-existent user"""
    response = client.get('/api/v1/users/99999')
    assert response.status_code == 404


def test_update_user(client, create_user):
    """Test updating an existing user"""
    # create_user does a post
    user_id = create_user("Bob", "Brown", "bob@example.com")

    # as the user was created w/ post, we can do a put
    response = client.put(f'/api/v1/users/{user_id}', json={
        # we change the first_name
        "first_name": "Robert",
        "last_name": "Brown",
        "email": "bob@example.com",
    })
    assert response.status_code == 200
    assert response.get_json()["first_name"] == "Robert"


def test_update_user_not_found(client):
    """Test updating a non-existent user"""
    response = client.put('/api/v1/users/99999', json={
        "first_name": "Unknown",
        "last_name": "User",
        "email": "unknown@example.com",
    })
    assert response.status_code == 404


def test_delete_user(client, create_user):
    """Test deleting an existing user"""
    # Create a user
    user_id = create_user("Charlie", "Chaplin", "charlie@example.com")

    # Delete the user
    response = client.delete(f'/api/v1/users/{user_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "User deleted successfully"

    # Verify the user is no longer retrievable
    response = client.get(f'/api/v1/users/{user_id}')
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "User not found"
