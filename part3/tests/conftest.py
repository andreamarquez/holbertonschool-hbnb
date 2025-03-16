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
        if response.status_code == 201:
            return response.get_json().get('id')
        return None
    return _create_user


@pytest.fixture
def create_amenity(client):
    """Helper function to create an amenity"""
    def _create_amenity(name):
        response = client.post('/api/v1/amenities/', json={
            "name": name
        })
        if response.status_code == 201:
            return response.get_json().get('id')
        return None
    return _create_amenity


@pytest.fixture
def create_place(client, auth_header):
    """Helper function to create a place"""
    def _create_place(
            title,
            description,
            price,
            latitude,
            longitude,
            owner_id,
            owner_email
            ):
        headers = auth_header(owner_email)

        response = client.post('/api/v1/places/', json={
            "title": title,
            "description": description,
            "price": price,
            "latitude": latitude,
            "longitude": longitude,
            "owner_id": owner_id,
            "amenities": ["wifi", "pool"]
        }, headers=headers)
        if response.status_code == 201:
            return response.get_json().get('id')
        return None
    return _create_place


@pytest.fixture
def auth_header(client):
    """Helper function to create an authorization header with a JWT token"""
    def _auth_header(email, password='12345678'):
        # Check if the user already exists
        response = client.post('/api/v1/auth/login', json={
            "email": email,
            "password": password
        })
        if response.status_code == 401:  # User does not exist
            # Create the user
            response = client.post('/api/v1/users/', json={
                "first_name": "John",
                "last_name": "Doe",
                "email": email,
                "password": password
            })
            assert response.status_code == 201, \
                "Failed to create user for authentication"

            # Authenticate the user
            response = client.post('/api/v1/auth/login', json={
                "email": email,
                "password": password
            })

        assert response.status_code == 200, "Failed to authenticate user"
        token = response.get_json().get('access_token')
        assert token is not None, "Failed to get access token"
        return {'Authorization': f'Bearer {token}'}
    return _auth_header
