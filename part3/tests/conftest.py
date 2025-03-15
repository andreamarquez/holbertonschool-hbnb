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


@pytest.fixture
def create_amenity(client):
    """Helper function to create an amenity"""
    def _create_amenity(name):
        response = client.post('/api/v1/amenities/', json={
            "name": name
        })
        return (
            response.get_json().get('id')
            if response.status_code == 201
            else None
        )
    return _create_amenity


@pytest.fixture
def create_place(client):
    """Helper function to create a place"""
    def _create_place(
            title,
            description,
            price,
            latitude,
            longitude,
            owner_id):
        response = client.post('/api/v1/places/', json={
            "title": title,
            "description": description,
            "price": price,
            "latitude": latitude,
            "longitude": longitude,
            "owner_id": owner_id,
            "amenities": ["wifi", "pool"]
        })
        return (
            response.get_json().get('id')
            if response.status_code == 201
            else None
        )
    return _create_place
