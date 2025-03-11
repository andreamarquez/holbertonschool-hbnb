from datetime import datetime
from .base_model import BaseModel
# from .user import User
# from .place import Place


class Review(BaseModel):
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
        place_dict = self.to_dict()
        place_dict['place_id'] = self.place
        place_dict.pop('place', None)
        place_dict['user_id'] = self.user
        place_dict.pop('user', None)
        return place_dict
