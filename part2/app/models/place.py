from datetime import datetime
from .base_model import BaseModel


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store related reviews ids
        self.amenities = []  # List to store related amenities ids
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def to_dict_with_owner_id(self):
        """Convert instance to dictionary with owner_id instead of owner"""
        place_dict = self.to_dict()
        place_dict['owner_id'] = self.owner
        place_dict.pop('owner', None)
        return place_dict
