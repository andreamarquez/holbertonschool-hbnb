import pytest


def test_create_review(client, create_user, create_place):
    """Test the creation of a review"""
    user_id = create_user("John", "Doe", "john.doe0111@example.com")
    place_id = create_place(
        "Beautiful Apartment",
        "A nice place near the beach",
        120.5,
        48.8566,
        2.3522,
        user_id)
    response = client.post('/api/v1/reviews/', json={
        "text": "Wow amazing!",
        "rating": 5,
        "user_id": user_id,
        "place_id": place_id
    })
    assert response.status_code == 201
    assert "id" in response.json
    assert response.json["text"] == "Wow amazing!"


def test_create_review_invalid_data(client, create_user, create_place):
    """Test creating a review with invalid data"""
    user_id = create_user("John", "Doe", "john.doe1111@example.com")
    place_id = create_place(
        "Beautiful Apartment",
        "A nice place near the beach",
        120.5,
        48.8566,
        2.3522,
        user_id)
    response = client.post('/api/v1/reviews/', json={
        "text": 5,
        "rating": "Weird, rating should be a number",
        "user_id": user_id,
        "place_id": place_id
    })
    assert response.status_code == 400
    assert "errors" in response.json


def test_get_all_reviews(client):
    """Test retrieving all reviews"""
    response = client.get('/api/v1/reviews/')
    assert response.status_code in [200, 404]


def test_get_review_by_id(client, create_user, create_place):
    """Test retrieving a specific review"""
    user_id = create_user("John", "Doe", "john.doe2111@example.com")
    place_id = create_place(
        "Beautiful Apartment",
        "A nice place near the beach",
        120.5,
        48.8566,
        2.3522,
        user_id)
    review_response = client.post('/api/v1/reviews/', json={
        "text": "Wow amazing!",
        "rating": 5,
        "user_id": user_id,
        "place_id": place_id
    })
    review_id = review_response.get_json().get('id')
    response = client.get(f'/api/v1/reviews/{review_id}')
    assert response.status_code == 200
    assert "id" in response.json


def test_update_review(client, create_user, create_place):
    """Test updating an existing review"""
    user_id = create_user("John", "Doe", "john.doe3111@example.com")
    place_id = create_place(
        "Beautiful Apartment",
        "A nice place near the beach",
        120.5,
        48.8566,
        2.3522,
        user_id)
    review_response = client.post('/api/v1/reviews/', json={
        "text": "Wow amazing!",
        "rating": 5,
        "user_id": user_id,
        "place_id": place_id
    })
    review_id = review_response.get_json().get('id')
    response = client.put(f'/api/v1/reviews/{review_id}', json={
        "text": "Awesome",
        "rating": 4
    })
    assert response.status_code == 200
    assert response.json["text"] == "Awesome"
    assert response.json["rating"] == 4


def test_delete_review(client, create_user, create_place):
    """Test deleting a review"""
    user_id = create_user("John", "Doe", "john.doe4111@example.com")
    place_id = create_place(
        "Beautiful Apartment",
        "A nice place near the beach",
        120.5,
        48.8566,
        2.3522,
        user_id)
    review_response = client.post('/api/v1/reviews/', json={
        "text": "Wow amazing!",
        "rating": 5,
        "user_id": user_id,
        "place_id": place_id
    })
    review_id = review_response.get_json().get('id')
    response = client.delete(f'/api/v1/reviews/{review_id}')
    assert response.status_code == 200
    assert response.json["message"] == "Review deleted successfully"


def test_get_reviews_by_place(client, create_user, create_place):
    """Test retrieving all reviews for a specific place"""
    user_id = create_user("John", "Doe", "john.doe5111@example.com")
    place_id = create_place(
        "Beautiful Apartment",
        "A nice place near the beach",
        120.5,
        48.8566,
        2.3522,
        user_id)
    client.post('/api/v1/reviews/', json={
        "text": "Wow amazing!",
        "rating": 5,
        "user_id": user_id,
        "place_id": place_id
    })
    response = client.get(f'/api/v1/reviews/places/{place_id}')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) > 0
    assert response.json[0]["place_id"] == place_id
