from datetime import datetime
from .base_model import BaseModel
from app.persistence.db import db

# Association table for many-to-many relationship between Place and Amenity
place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'
    
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    owner = db.Column(db.String(36), nullable=False)  # Owner is id of user who owns the place

    # Relationships
    amenities = db.relationship('Amenity', secondary=place_amenity, backref='places')
    reviews = db.relationship('Review', backref='place_obj', cascade='all, delete-orphan')

    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)

    def to_dict_with_owner_id(self):
        place_dict = self.to_dict()
        place_dict['owner_id'] = self.owner
        place_dict.pop('owner', None)
        # Add amenities as list of ids
        place_dict['amenities'] = [a.id for a in self.amenities]
        # Add reviews as list of ids
        place_dict['reviews'] = [r.id for r in self.reviews]
        return place_dict
