from datetime import datetime
from .base_model import BaseModel
from app.persistence.db import db
from sqlalchemy.orm import relationship

# Association table for many-to-many relationship between Place and Amenity
place_amenity = db.Table(
    'place_amenity',
    db.Column(
        'place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True
    ),
    db.Column(
        'amenity_id',
        db.String(36),
        db.ForeignKey('amenities.id'),
        primary_key=True
    )
)


class Place(BaseModel, db.Model):
    __tablename__ = 'places'

    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    owner = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)

    # Relationships
    amenities = relationship(
        'Amenity', secondary='place_amenity', backref='places')
    reviews = relationship(
        'Review', backref='place_obj', cascade='all, delete-orphan')

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
