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
def create_amenity(client):
    """Helper function to create an amenity"""
    def _create_amenity(name):
        response = client.post('/api/v1/amenities/', json={
            "name": name
        })
        return response.get_json().get('id') if response.status_code == 201 else None
    return _create_amenity

def test_create_amenity(client):
    """Test the creation of an amenity"""
    response = client.post('/api/v1/amenities/', json={
        "name": "WiFi"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["name"] == "WiFi"

def test_create_amenity_fail_missing_data(client):
    """Test creating an amenity with missing data"""
    response = client.post('/api/v1/amenities/', json={})
    assert response.status_code == 400
    data = response.get_json()
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid input data"

def test_get_amenity(client, create_amenity):
    """Test retrieving an amenity by ID"""
    amenity_id = create_amenity("TV")
    response = client.get(f'/api/v1/amenities/{amenity_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == amenity_id
    assert data["name"] == "TV"

def test_get_amenities(client, create_amenity):
    """Test retrieving the list of amenities"""
    amenity_id = create_amenity("Pool")
    response = client.get('/api/v1/amenities/')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    pool = next((amenity for amenity in data if amenity["name"] == "Pool"), None)

    expected_amenity = {
        "id": amenity_id,
        "name": "Pool",
        "created_at": pool["created_at"],  # Use the actual timestamp from the response
        "updated_at": pool["updated_at"]   # Use the actual timestamp from the response
    }

    assert pool is not None
    assert pool == expected_amenity

def test_get_non_existent_amenity(client):
    """Test retrieving a non-existent amenity"""
    response = client.get('/api/v1/amenities/non_existent_id')
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Amenity not found"

def test_update_amenity(client, create_amenity):
    """Test updating an existing amenity"""
    # Create an amenity
    amenity_id = create_amenity("Gym")

    # Update the amenity
    response = client.put(f'/api/v1/amenities/{amenity_id}', json={
        "name": "Fitness Center"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Fitness Center"

    # Verify the amenity was updated
    response = client.get(f'/api/v1/amenities/{amenity_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Fitness Center"

def test_update_non_existent_amenity(client):
    """Test updating a non-existent amenity"""
    response = client.put('/api/v1/amenities/non_existent_id', json={
        "name": "Non Existent Amenity"
    })
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Amenity not found"

def test_delete_amenity(client, create_amenity):
    """Test deleting an existing amenity"""
    # Create an amenity
    amenity_id = create_amenity("Sauna")

    # Delete the amenity
    response = client.delete(f'/api/v1/amenities/{amenity_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Amenity deleted successfully"

    # Verify the amenity is no longer retrievable
    response = client.get(f'/api/v1/amenities/{amenity_id}')
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Amenity not found"

