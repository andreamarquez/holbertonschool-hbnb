import uuid
from datetime import datetime

class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp
    
    def to_dict(self):
        """Convert instance to dictionary"""
        dictionary = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime):
                dictionary[key] = value.isoformat()
            elif hasattr(value, 'to_dict'):
                dictionary[key] = value.to_dict()
            else:
                dictionary[key] = value
        return dictionary
