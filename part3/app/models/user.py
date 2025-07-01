from datetime import datetime
from .base_model import BaseModel
from app.utils.encryption import bcrypt
from app.persistence.db import db


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.set_password(password)

    def set_password(self, password):
        # Check if the password is already hashed
        # (starts with $2 and has a valid bcrypt length)
        if password.startswith("$2") and len(password) == 60:
            self.password
        else:
            self.hash_password(password)

    def hash_password(self, password):
        # Hashes the password before storing it
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        # Verifies if the provided password matches the hashed password
        return bcrypt.check_password_hash(self.password, password)
