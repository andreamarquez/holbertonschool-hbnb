import pytest
import uuid


def test_create_review(client, create_user, create_place, auth_header):
    """Test the creation of a review"""
    user_email = f"john.doe0110{uuid.uuid4().hex[:6]}@example.com"
    user_id = create_user("John", "Doe", user_email)
    headers = auth_header(user_email)

    owner_email = f"placius.ownerious1{uuid.uuid4().hex[:6]}@example.com"
    owner_id = create_user("Placius", "Ownerious", owner_email)

    place_id = create_place(
        f"Beautiful Apartment {uuid.uuid4().hex[:4]}",
        "A nice place near the beach",
        120.5,
        48.8566,
        2.3522,
        owner_id,
        owner_email)

    response = client.post('/api/v1/reviews/', json={
        "text": "Wow amazing!",
        "rating": 5,
        "user_id": user_id,
        "place_id": place_id
    }, headers=headers)
    assert response.status_code == 201
    assert "id" in response.json
    assert response.json["text"] == "Wow amazing!"


def test_create_duplicate_review(
        client, create_user, create_place, auth_header):
    """Test that a user cannot create multiple reviews for the same place"""
    user_email = f"john.doe0111{uuid.uuid4().hex[:6]}@example.com"
    user_id = create_user("John", "Doe", user_email)
    headers = auth_header(user_email)

    owner_email = f"placius.ownerious2{uuid.uuid4().hex[:6]}@example.com"
    owner_id = create_user("Placius", "Ownerious", owner_email)

    place_id = create_place(
        f"Beautiful Apartment {uuid.uuid4().hex[:4]}",
        "A nice place near the beach",
        120.5,
        48.8566,
        2.3522,
        owner_id,
        owner_email)

    # First review creation
    response1 = client.post('/api/v1/reviews/', json={
        "text": "Wow amazing!",
        "rating": 5,
        "user_id": user_id,
        "place_id": place_id
    }, headers=headers)
    assert response1.status_code == 201

    # Attempt to create a second review for the same place
    response2 = client.post('/api/v1/reviews/', json={
        "text": "Still amazing!",
        "rating": 4,
        "user_id": user_id,
        "place_id": place_id
    }, headers=headers)
    assert response2.status_code == 400
    assert response2.json["message"] == "You have already reviewed this place"


def test_create_review_invalid_data(
        client, create_user, create_place, auth_header):
    """Test creating a review with invalid data"""
    user_email = f"john.doe1111{uuid.uuid4().hex[:6]}@example.com"
    user_id = create_user("John", "Doe", user_email)
    headers = auth_header(user_email)

    owner_email = f"placius.ownerious3{uuid.uuid4().hex[:6]}@example.com"
    owner_id = create_user("Placius", "Ownerious", owner_email)

    place_id = create_place(
        f"Beautiful Apartment {uuid.uuid4().hex[:4]}",
        "A nice place near the beach",
        120.5,
        48.8566,
        2.3522,
        owner_id,
        owner_email)

    response = client.post('/api/v1/reviews/', json={
        "text": 5,
        "rating": "Weird, rating should be a number",
        "user_id": user_id,
        "place_id": place_id
    }, headers=headers)
    assert response.status_code == 400
    assert "errors" in response.json
    assert response.json["errors"]["rating"] == \
        "'Weird, rating should be a number' is not of type 'integer'"
    assert response.json["errors"]["text"] == "5 is not of type 'string'"


def test_get_all_reviews(client, auth_header):
    """Test retrieving all reviews"""
    unique_email = f"john.doe{uuid.uuid4().hex[:6]}@example.com"
    headers = auth_header(unique_email)
    response = client.get('/api/v1/reviews/', headers=headers)
    assert response.status_code in [200, 404]


def test_get_review_by_id(client, create_user, create_place, auth_header):
    """Test retrieving a specific review"""
    user_email = f"john.doe2111{uuid.uuid4().hex[:6]}@example.com"
    user_id = create_user("John", "Doe", user_email)
    headers = auth_header(user_email)

    owner_email = f"placius.ownerious4{uuid.uuid4().hex[:6]}@example.com"
    owner_id = create_user("Placius", "Ownerious", owner_email)

    place_id = create_place(
        f"Beautiful Apartment {uuid.uuid4().hex[:4]}",
        "A nice place near the beach",
        120.5,
        48.8566,
        2.3522,
        owner_id,
        owner_email)

    review_response = client.post('/api/v1/reviews/', json={
        "text": "Wow amazing!",
        "rating": 5,
        "user_id": user_id,
        "place_id": place_id
    }, headers=headers)
    review_id = review_response.get_json().get('id')
    response = client.get(f'/api/v1/reviews/{review_id}', headers=headers)
    assert response.status_code == 200
    assert "id" in response.json


def test_update_review(client, create_user, create_place, auth_header):
    """Test updating an existing review"""
    user_email = f"john.doe3111{uuid.uuid4().hex[:6]}@example.com"
    user_id = create_user("John", "Doe", user_email)
    headers = auth_header(user_email)

    owner_email = f"placius.ownerious5{uuid.uuid4().hex[:6]}@example.com"
    owner_id = create_user("Placius", "Ownerious", owner_email)

    place_id = create_place(
        f"Beautiful Apartment {uuid.uuid4().hex[:4]}",
        "A nice place near the beach",
        120.5,
        48.8566,
        2.3522,
        owner_id,
        owner_email)

    review_response = client.post('/api/v1/reviews/', json={
        "text": "Wow amazing!",
        "rating": 5,
        "user_id": user_id,
        "place_id": place_id
    }, headers=headers)
    review_id = review_response.get_json().get('id')
    response = client.put(f'/api/v1/reviews/{review_id}', json={
        "text": "Awesome",
        "rating": 4
    }, headers=headers)
    assert response.status_code == 200
    assert response.json["text"] == "Awesome"
    assert response.json["rating"] == 4


def test_delete_review(client, create_user, create_place, auth_header):
    """Test deleting a review"""
    user_email = f"john.doe4111{uuid.uuid4().hex[:6]}@example.com"
    user_id = create_user("John", "Doe", user_email)
    headers = auth_header(user_email)

    owner_email = f"placius.ownerious6{uuid.uuid4().hex[:6]}@example.com"
    owner_id = create_user("Placius", "Ownerious", owner_email)

    place_id = create_place(
        f"Beautiful Apartment {uuid.uuid4().hex[:4]}",
        "A nice place near the beach",
        120.5,
        48.8566,
        2.3522,
        owner_id,
        owner_email)

    review_response = client.post('/api/v1/reviews/', json={
        "text": "Wow amazing!",
        "rating": 5,
        "user_id": user_id,
        "place_id": place_id
    }, headers=headers)
    review_id = review_response.get_json().get('id')
    response = client.delete(f'/api/v1/reviews/{review_id}', headers=headers)
    assert response.status_code == 200
    assert response.json["message"] == "Review deleted successfully"


def test_get_reviews_by_place(client, create_user, create_place, auth_header):
    """Test retrieving all reviews for a specific place"""
    user_email = f"john.doe5111{uuid.uuid4().hex[:6]}@example.com"
    user_id = create_user("John", "Doe", user_email)
    headers = auth_header(user_email)

    owner_email = f"placius.ownerious7{uuid.uuid4().hex[:6]}@example.com"
    owner_id = create_user("Placius", "Ownerious", owner_email)

    place_id = create_place(
        f"Beautiful Apartment {uuid.uuid4().hex[:4]}",
        "A nice place near the beach",
        120.5,
        48.8566,
        2.3522,
        owner_id,
        owner_email)

    client.post('/api/v1/reviews/', json={
        "text": "Wow amazing!",
        "rating": 5,
        "user_id": user_id,
        "place_id": place_id
    }, headers=headers)
    response = client.get(
        f'/api/v1/reviews/places/{place_id}', headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) > 0
    assert response.json[0]["place_id"] == place_id


def test_update_review_restrictions(
        client, create_user, create_place, auth_header):
    """Test restrictions on updating a review"""
    # Create the original author of the review
    author_email = f"john.doe6111{uuid.uuid4().hex[:6]}@example.com"
    author_id = create_user("John", "Doe", author_email)
    author_headers = auth_header(author_email)

    # Create another user who will attempt to update the review
    other_user_email = f"jane.doe7111{uuid.uuid4().hex[:6]}@example.com"
    other_user_id = create_user("Jane", "Doe", other_user_email)
    other_user_headers = auth_header(other_user_email)

    # Create a place owned by a third user
    owner_email = f"placius.ownerious8{uuid.uuid4().hex[:6]}@example.com"
    owner_id = create_user("Placius", "Ownerious", owner_email)

    place_id = create_place(
        f"Beautiful Apartment {uuid.uuid4().hex[:4]}",
        "A nice place near the beach",
        120.5,
        48.8566,
        2.3522,
        owner_id,
        owner_email
    )

    # Create a review as the author
    review_response = client.post('/api/v1/reviews/', json={
        "text": "Great place!",
        "rating": 5,
        "user_id": author_id,
        "place_id": place_id
    }, headers=author_headers)
    review_id = review_response.get_json().get('id')

    # Try to update the review as another user
    response = client.put(f'/api/v1/reviews/{review_id}', json={
        "text": "Actually, not so great",
        "rating": 2
    }, headers=other_user_headers)
    assert response.status_code == 403
    assert response.json["message"] == "Unauthorized action"


def test_delete_review_restrictions(
        client, create_user, create_place, auth_header):
    """Test restrictions on deleting a review"""
    # Create the original author of the review
    author_email = f"john.doe8111{uuid.uuid4().hex[:6]}@example.com"
    author_id = create_user("John", "Doe", author_email)
    author_headers = auth_header(author_email)

    # Create another user who will attempt to delete the review
    other_user_email = f"jane.doe9111{uuid.uuid4().hex[:6]}@example.com"
    other_user_id = create_user("Jane", "Doe", other_user_email)
    other_user_headers = auth_header(other_user_email)

    # Create a place owned by a third user
    owner_email = f"placius.ownerious9{uuid.uuid4().hex[:6]}@example.com"
    owner_id = create_user("Placius", "Ownerious", owner_email)

    place_id = create_place(
        f"Beautiful Apartment {uuid.uuid4().hex[:4]}",
        "A nice place near the beach",
        120.5,
        48.8566,
        2.3522,
        owner_id,
        owner_email
    )

    # Create a review as the author
    review_response = client.post('/api/v1/reviews/', json={
        "text": "Great place!",
        "rating": 5,
        "user_id": author_id,
        "place_id": place_id
    }, headers=author_headers)
    review_id = review_response.get_json().get('id')

    # Try to delete the review as another user
    response = client.delete(
        f'/api/v1/reviews/{review_id}',
        headers=other_user_headers)
    assert response.status_code == 403
    assert response.json["message"] == "Unauthorized action"

    # Delete the review as the author (should succeed)
    delete_response_author = client.delete(
        f'/api/v1/reviews/{review_id}',
        headers=author_headers)
    assert delete_response_author.status_code == 200
    assert delete_response_author.json["message"] == \
        "Review deleted successfully"


# Add a fixture to create amenities and return their IDs
@pytest.fixture
def create_amenities(client):
    def _create_amenities(names):
        ids = []
        for name in names:
            response = client.post('/api/v1/amenities/', json={"name": name})
            assert response.status_code == 201
            ids.append(response.get_json()["id"])
        return ids
    return _create_amenities


@pytest.fixture
def create_place(client, create_user, auth_header, create_amenities):
    def _create_place(
        title,
        description,
        price,
        latitude,
        longitude,
        owner_id,
        owner_email,
        amenity_names=None
    ):
        headers = auth_header(owner_email)
        amenity_ids = create_amenities(
            amenity_names or [f"wifi_{uuid.uuid4().hex[:4]}"])
        response = client.post(
            '/api/v1/places/',
            json={
                "title": title,
                "description": description,
                "price": price,
                "latitude": latitude,
                "longitude": longitude,
                "owner_id": owner_id,
                "amenities": amenity_ids
            },
            headers=headers
        )
        assert response.status_code == 201
        return response.get_json().get('id')
    return _create_place
