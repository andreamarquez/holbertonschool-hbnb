import pytest


def test_create_review(client, create_user, create_place, auth_header):
    """Test the creation of a review"""
    user_email = "john.doe0110@example.com"
    user_id = create_user("John", "Doe", user_email)
    headers = auth_header(user_email)

    owner_email = "placius.ownerious1@example.com"
    owner_id = create_user("Placius", "Ownerious", owner_email)

    place_id = create_place(
        "Beautiful Apartment",
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
    user_email = "john.doe0111@example.com"
    user_id = create_user("John", "Doe", user_email)
    headers = auth_header(user_email)

    owner_email = "placius.ownerious2@example.com"
    owner_id = create_user("Placius", "Ownerious", owner_email)

    place_id = create_place(
        "Beautiful Apartment",
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
    user_email = "john.doe1111@example.com"
    user_id = create_user("John", "Doe", user_email)
    headers = auth_header(user_email)

    owner_email = "placius.ownerious3@example.com"
    owner_id = create_user("Placius", "Ownerious", owner_email)

    place_id = create_place(
        "Beautiful Apartment",
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
    headers = auth_header("john.doe@example.com")
    response = client.get('/api/v1/reviews/', headers=headers)
    assert response.status_code in [200, 404]


def test_get_review_by_id(client, create_user, create_place, auth_header):
    """Test retrieving a specific review"""
    user_email = "john.doe2111@example.com"
    user_id = create_user("John", "Doe", user_email)
    headers = auth_header(user_email)

    owner_email = "placius.ownerious4@example.com"
    owner_id = create_user("Placius", "Ownerious", owner_email)

    place_id = create_place(
        "Beautiful Apartment",
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
    user_email = "john.doe3111@example.com"
    user_id = create_user("John", "Doe", user_email)
    headers = auth_header(user_email)

    owner_email = "placius.ownerious5@example.com"
    owner_id = create_user("Placius", "Ownerious", owner_email)

    place_id = create_place(
        "Beautiful Apartment",
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
    user_email = "john.doe4111@example.com"
    user_id = create_user("John", "Doe", user_email)
    headers = auth_header(user_email)

    owner_email = "placius.ownerious6@example.com"
    owner_id = create_user("Placius", "Ownerious", owner_email)

    place_id = create_place(
        "Beautiful Apartment",
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
    user_email = "john.doe5111@example.com"
    user_id = create_user("John", "Doe", user_email)
    headers = auth_header(user_email)

    owner_email = "placius.ownerious7@example.com"
    owner_id = create_user("Placius", "Ownerious", owner_email)

    place_id = create_place(
        "Beautiful Apartment",
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
    author_email = "john.doe6111@example.com"
    author_id = create_user("John", "Doe", author_email)
    author_headers = auth_header(author_email)

    # Create another user who will attempt to update the review
    other_user_email = "jane.doe7111@example.com"
    other_user_id = create_user("Jane", "Doe", other_user_email)
    other_user_headers = auth_header(other_user_email)

    # Create a place owned by a third user
    owner_email = "placius.ownerious8@example.com"
    owner_id = create_user("Placius", "Ownerious", owner_email)

    place_id = create_place(
        "Beautiful Apartment",
        "A nice place near the beach",
        120.5,
        48.8566,
        2.3522,
        owner_id,
        owner_email
    )

    # Original author creates a review
    review_response = client.post('/api/v1/reviews/', json={
        "text": "Wow amazing!",
        "rating": 5,
        "user_id": author_id,
        "place_id": place_id
    }, headers=author_headers)
    assert review_response.status_code == 201
    review_id = review_response.get_json().get('id')

    # Attempt to update the review by another user
    update_response = client.put(f'/api/v1/reviews/{review_id}', json={
        "text": "Not so amazing anymore",
        "rating": 3
    }, headers=other_user_headers)
    assert update_response.status_code == 403
    assert update_response.json["message"] == "Unauthorized action"

    # Original author updates the review
    update_response_author = client.put(f'/api/v1/reviews/{review_id}', json={
        "text": "Still amazing!",
        "rating": 4
    }, headers=author_headers)
    assert update_response_author.status_code == 200
    assert update_response_author.json["text"] == "Still amazing!"
    assert update_response_author.json["rating"] == 4


def test_delete_review_restrictions(
        client, create_user, create_place, auth_header):
    """Test restrictions on deleting a review"""
    # Create the original author of the review
    author_email = "john.doe8111@example.com"
    author_id = create_user("John", "Doe", author_email)
    author_headers = auth_header(author_email)

    # Create another user who will attempt to delete the review
    other_user_email = "jane.doe9111@example.com"
    other_user_id = create_user("Jane", "Doe", other_user_email)
    other_user_headers = auth_header(other_user_email)

    # Create a place owned by a third user
    owner_email = "placius.ownerious9@example.com"
    owner_id = create_user("Placius", "Ownerious", owner_email)

    place_id = create_place(
        "Beautiful Apartment",
        "A nice place near the beach",
        120.5,
        48.8566,
        2.3522,
        owner_id,
        owner_email
    )

    # Original author creates a review
    review_response = client.post('/api/v1/reviews/', json={
        "text": "Wow amazing!",
        "rating": 5,
        "user_id": author_id,
        "place_id": place_id
    }, headers=author_headers)
    assert review_response.status_code == 201
    review_id = review_response.get_json().get('id')

    # Attempt to delete the review by another user
    delete_response = client.delete(
        f'/api/v1/reviews/{review_id}', headers=other_user_headers)
    assert delete_response.status_code == 403
    assert delete_response.json["message"] == "Unauthorized action"

    # Original author deletes the review
    delete_response_author = client.delete(
        f'/api/v1/reviews/{review_id}', headers=author_headers)
    assert delete_response_author.status_code == 200
    assert delete_response_author.json["message"] == \
        "Review deleted successfully"
