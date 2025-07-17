from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.places import api as places_ns
from app.api.v1.auth import api as auth_ns
from app.utils.encryption import bcrypt
from app.persistence.db import db
from config import config

# Instantiate JWTManager
jwt = JWTManager()


def create_app(config_name="development"):
    app = Flask(__name__)
    config_class = config[config_name]
    app.config.from_object(config_class)
    db.init_app(app)

    # Initialize Bcrypt with the Flask app
    bcrypt.init_app(app)

    app.config['JWT_ERROR_MESSAGE_KEY'] = 'message'

    # Initialize JWTManager with the Flask app
    jwt.init_app(app)

    # Enable CORS for all /api/* endpoints from local front-end origins
    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5500", "http://127.0.0.1:5500"]}}, supports_credentials=True)

    # Create database tables
    with app.app_context():
        db.create_all()

    # Add security definitions for Swagger
    authorizations = {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description':
                'JWT Auth header (Bearer scheme). Example: "Bearer {token}"'
        }
    }

    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/',
        authorizations=authorizations,
        security='Bearer'
    )

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    return app


__all__ = ['create_app']
