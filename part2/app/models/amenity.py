from datetime import datetime
from .base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
