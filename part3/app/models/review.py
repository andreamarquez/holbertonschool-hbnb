from datetime import datetime
from .base_model import BaseModel
from app.persistence.db import db
# from .user import User
# from .place import Place


class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place = db.Column(
        db.String(36), db.ForeignKey('places.id'), nullable=False
    )
    user = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def to_dict_with_ids(self):
        """Convert instance to dictionary with owner_id instead of owner"""
        review_dict = self.to_dict()
        review_dict['place_id'] = self.place
        review_dict.pop('place', None)
        review_dict['user_id'] = self.user
        review_dict.pop('user', None)
        return review_dict
