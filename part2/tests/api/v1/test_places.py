import pytest
from app import create_app
from app.services.facade import HBnBFacade


@pytest.fixture(scope='session')
def app():
    """Initialize the Flask application in test mode"""
    app = create_app(config_name="testing")
    return app


@pytest.fixture(scope='session')
def client(app):
    """Create a test client for the Flask application"""
    return app.test_client()


@pytest.fixture(scope='session')
def facade():
    """Initialize the HBnBFacade"""
    return HBnBFacade()


@pytest.fixture(scope='session')
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


def test_create_place(client, create_user):
    """Test the creation of a place"""
    # Create a user to be the owner of the place
    owner_id = create_user("John", "Doe", "john.doe@example.com")
    assert owner_id is not None, "Failed to create user"

    response = client.post('/api/v1/places/', json={
        "title": "Beautiful Apartment",
        "description": "A nice place near the beach",
        "price": 120.5,
        "latitude": 48.8566,
        "longitude": 2.3522,
        "owner_id": owner_id,
        "amenities": ["wifi", "pool"]
    })
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["title"] == "Beautiful Apartment"
    assert data["owner_id"] == owner_id


def test_get_places(client):
    """Test retrieving the list of places"""
    response = client.get('/api/v1/places/')
    assert response.status_code == 200


def test_get_place_not_found(client):
    """Test retrieving a non-existent place"""
    response = client.get('/api/v1/places/999')
    assert response.status_code == 404


def test_update_place(client, create_user):
    """Test updating an existing place"""
    # Create a user to be the owner of the place
    owner_id = create_user("Mary", "Doe", "mary.doe@example.com")
    assert owner_id is not None, "Failed to create user"

    # Create a place
    response = client.post('/api/v1/places/', json={
        "title": "Beautiful Apartment",
        "description": "A nice place near the beach",
        "price": 120.5,
        "latitude": 48.8566,
        "longitude": 2.3522,
        "owner_id": owner_id,
        "amenities": ["wifi", "pool"]
    })
    place_id = response.get_json().get('id')
    assert response.status_code == 201

    # Update the place
    response = client.put(f'/api/v1/places/{place_id}', json={
        "title": "Updated Apartment",
        "description": "An updated description",
        "price": 150.0,
        "latitude": 48.8566,
        "longitude": 2.3522,
        "owner_id": owner_id,
        "amenities": ["wifi", "gym"]
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Updated Apartment"
    assert data["description"] == "An updated description"
    assert data["price"] == 150.0


def test_delete_place(client, create_user):
    """Test deleting an existing place"""
    # Create a user to be the owner of the place
    owner_id = create_user("Duper", "Doe", "duper.doe@example.com")
    assert owner_id is not None, "Failed to create user"

    # Create a place
    response = client.post('/api/v1/places/', json={
        "title": "Beautiful Apartment",
        "description": "A nice place near the beach",
        "price": 120.5,
        "latitude": 48.8566,
        "longitude": 2.3522,
        "owner_id": owner_id,
        "amenities": ["wifi", "pool"]
    })
    place_id = response.get_json().get('id')
    assert response.status_code == 201

    # Delete the place
    response = client.delete(f'/api/v1/places/{place_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Deleted"

    # Verify the place is no longer retrievable
    response = client.get(f'/api/v1/places/{place_id}')
    assert response.status_code == 404
    data = response.get_json()
    assert data["message"] == "Not found"


def test_create_place_missing_data(client):
    """Test creating a place with missing data"""

    # Attempt to create a place with missing title
    response = client.post('/api/v1/places/', json={
        "description": "A nice place near the beach",
        "price": 120.5,
        "latitude": 48.8566,
        "longitude": 2.3522,
        "owner_id": "azertyui",
        "amenities": ["wifi", "pool"]
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "message" in data
    assert "errors" in data
    assert data["errors"]["title"] == "'title' is a required property"


def test_create_place_invalid_data(client, create_user):
    """Test creating a place with invalid data"""
    # Create a user to be the owner of the place
    owner_id = create_user("Hyper", "Doe", "hyper.doe@example.com")
    assert owner_id is not None, "Failed to create user"

    # Attempt to create a place with invalid price
    response = client.post('/api/v1/places/', json={
        "title": "Beautiful Apartment",
        "description": "A nice place near the beach",
        "price": "invalid_price",
        "latitude": 48.8566,
        "longitude": 2.3522,
        "owner_id": owner_id,
        "amenities": ["wifi", "pool"]
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "message" in data
