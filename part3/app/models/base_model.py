from app.persistence.db import db
import uuid
from datetime import datetime


class BaseModel(db.Model):
    __abstract__ = True  # This ensures SQLAlchemy does not create a table for BaseModel

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.utcnow()

    def update(self, data):
        """Update the attributes of the object based on the provided
        dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp

    def to_dict(self):
        """Convert instance to dictionary"""
        dictionary = {}
        for key in self.__mapper__.c.keys():  # Use SQLAlchemy's column keys
            value = getattr(self, key)
            if isinstance(value, datetime):
                dictionary[key] = value.isoformat()  # Convert datetime to ISO format
            else:
                dictionary[key] = value
        return dictionary
