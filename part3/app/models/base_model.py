from app.persistence.db import db
import uuid
from datetime import datetime


class BaseModel(db.Model):
    # This ensures SQLAlchemy does not create a table for BaseModel
    __abstract__ = True

    id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow
    )
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def save(self):
        """Update updated_at and save to the database"""
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """Update the model with a dictionary of new values"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        """Convert instance to dictionary"""
        dictionary = {}
        # Use SQLAlchemy's column keys
        for key in self.__mapper__.c.keys():
            value = getattr(self, key)
            if isinstance(value, datetime):
                # Convert datetime to ISO format
                dictionary[key] = value.isoformat()
            else:
                dictionary[key] = value
        return dictionary
