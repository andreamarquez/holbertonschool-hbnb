from datetime import datetime
from .base_model import BaseModel
from app.persistence.db import db


class Amenity(BaseModel):
    __tablename__ = 'amenities'
    
    name = db.Column(db.String(128), nullable=False)

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
