import pytest
import uuid

@pytest.fixture
def create_amenities(client):
    """Helper to create amenities and return their IDs"""
    def _create_amenities(names):
        ids = []
        for name in names:
            response = client.post('/api/v1/amenities/', json={"name": name})
            assert response.status_code == 201
            ids.append(response.get_json()["id"])
        return ids
    return _create_amenities


def test_create_place(client, create_user, auth_header, create_amenities):
    """Test the creation of a place"""
    # Create a user to be the owner of the place
    unique_email = f"john.doe{uuid.uuid4().hex[:6]}@example.com"
    owner_id = create_user("John", "Doe", unique_email)
    assert owner_id is not None, "Failed to create user"

    headers = auth_header(unique_email)
    amenity_names = [f"wifi_{uuid.uuid4().hex[:4]}", f"pool_{uuid.uuid4().hex[:4]}"]
    amenity_ids = create_amenities(amenity_names)

    response = client.post('/api/v1/places/', json={
        "title": f"Beautiful Apartment {uuid.uuid4().hex[:4]}",
        "description": "A nice place near the beach",
        "price": 120.5,
        "latitude": 48.8566,
        "longitude": 2.3522,
        "owner_id": owner_id,
        "amenities": amenity_ids
    }, headers=headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data is not None, "Response JSON is None"
    assert "id" in data
    assert data["title"].startswith("Beautiful Apartment")
    assert data["owner_id"] == owner_id
    assert set(data["amenities"]) == set(amenity_ids)


def test_get_places(client):
    """Test retrieving the list of places"""
    response = client.get('/api/v1/places/')
    assert response.status_code == 200
    data = response.get_json()
    assert data is not None, "Response JSON is None"


def test_get_place_not_found(client):
    """Test retrieving a non-existent place"""
    response = client.get('/api/v1/places/999')
    assert response.status_code == 404
    data = response.get_json()
    assert data is not None, "Response JSON is None"


def test_update_place(client, create_user, auth_header):
    """Test updating an existing place"""
    # Create a user to be the owner of the place
    unique_email = f"mary.doe{uuid.uuid4().hex[:6]}@example.com"
    owner_id = create_user("Mary", "Doe", unique_email)
    assert owner_id is not None, "Failed to create user"

    headers = auth_header(unique_email)

    # Create a place
    response = client.post('/api/v1/places/', json={
        "title": f"Beautiful Apartment {uuid.uuid4().hex[:4]}",
        "description": "A nice place near the beach",
        "price": 120.5,
        "latitude": 48.8566,
        "longitude": 2.3522,
        "owner_id": owner_id,
        "amenities": []
    }, headers=headers)
    place_id = response.get_json().get('id')
    assert response.status_code == 201
    assert place_id is not None, "Failed to create place"

    # Update the place
    response = client.put(f'/api/v1/places/{place_id}', json={
        "title": "Updated Apartment",
        "description": "An updated description",
        "price": 150.0,
        "latitude": 48.8566,
        "longitude": 2.3522,
        "owner_id": owner_id,
        "amenities": []
    }, headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data is not None, "Response JSON is None"
    assert data["title"] == "Updated Apartment"
    assert data["description"] == "An updated description"
    assert data["price"] == 150.0


def test_delete_place(client, create_user, auth_header):
    """Test deleting an existing place"""
    # Create a user to be the owner of the place
    unique_email = f"duper.doe{uuid.uuid4().hex[:6]}@example.com"
    owner_id = create_user("Duper", "Doe", unique_email)
    assert owner_id is not None, "Failed to create user"

    headers = auth_header(unique_email)

    # Create a place
    response = client.post('/api/v1/places/', json={
        "title": f"Beautiful Apartment {uuid.uuid4().hex[:4]}",
        "description": "A nice place near the beach",
        "price": 120.5,
        "latitude": 48.8566,
        "longitude": 2.3522,
        "owner_id": owner_id,
        "amenities": []
    }, headers=headers)
    place_id = response.get_json().get('id')
    assert response.status_code == 201
    assert place_id is not None, "Failed to create place"

    # Delete the place
    response = client.delete(f'/api/v1/places/{place_id}', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data is not None, "Response JSON is None"
    assert data["message"] == "Deleted"

    # Verify the place is no longer retrievable
    response = client.get(f'/api/v1/places/{place_id}')
    assert response.status_code == 404
    data = response.get_json()
    assert data is not None, "Response JSON is None"
    assert data["message"] == "Not found"


def test_create_place_missing_data(client, auth_header):
    """Test creating a place with missing data"""
    unique_email = f"john.doe{uuid.uuid4().hex[:6]}@example.com"
    headers = auth_header(unique_email)

    # Attempt to create a place with missing title
    response = client.post('/api/v1/places/', json={
        "description": "A nice place near the beach",
        "price": 120.5,
        "latitude": 48.8566,
        "longitude": 2.3522,
        "owner_id": "azertyui",
        "amenities": []
    }, headers=headers)
    assert response.status_code == 400
    data = response.get_json()
    assert data is not None, "Response JSON is None"
    assert "message" in data
    assert "errors" in data
    assert data["errors"]["title"] == "'title' is a required property"


def test_create_place_invalid_data(client, create_user, auth_header):
    """Test creating a place with invalid data"""
    # Create a user to be the owner of the place
    unique_email = f"hyper.doe{uuid.uuid4().hex[:6]}@example.com"
    owner_id = create_user("Hyper", "Doe", unique_email)
    assert owner_id is not None, "Failed to create user"

    headers = auth_header(unique_email)

    # Attempt to create a place with invalid price
    response = client.post('/api/v1/places/', json={
        "title": f"Beautiful Apartment {uuid.uuid4().hex[:4]}",
        "description": "A nice place near the beach",
        "price": "invalid_price",
        "latitude": 48.8566,
        "longitude": 2.3522,
        "owner_id": owner_id,
        "amenities": []
    }, headers=headers)
    assert response.status_code == 400
    data = response.get_json()
    assert data is not None, "Response JSON is None"
    assert "message" in data
