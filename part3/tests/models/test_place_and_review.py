from app.models.place import Place
from app.models.user import User
from app.models.review import Review
from app.persistence.db import db
import pytest
import uuid


def test_place_creation(app):
    """Test place creation with proper app context"""
    with app.app_context():
        owner = User(
            first_name="Alice",
            last_name="Smith",
            email=f"alice.smith{uuid.uuid4().hex[:6]}@example.com",
            password="securepassword"
        )
        db.session.add(owner)
        db.session.commit()

        place = Place(
            title="Cozy Apartment",
            description="A nice place to stay",
            price=100,
            latitude=37.7749,
            longitude=-122.4194,
            owner=owner.id
        )
        db.session.add(place)
        db.session.commit()

        review = Review(
            text="Great stay!",
            rating=5,
            place=place.id,
            user=owner.id)
        db.session.add(review)
        place.add_review(review)
        db.session.commit()

        # Query back
        queried_place = Place.query.get(place.id)
        queried_review = Review.query.get(review.id)
        assert queried_place.title == "Cozy Apartment"
        assert queried_place.price == 100
        assert len(queried_place.reviews) == 1
        assert queried_place.reviews[0].text == "Great stay!"
        assert queried_review.place == place.id
        assert queried_review.user == owner.id
        print("Place creation and relationship test passed!")
