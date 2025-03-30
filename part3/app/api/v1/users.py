from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('users', description='User operations')

# Define user model for input validation and documentation
user_model = api.model(
    'User', {
        'first_name': fields.String(
            required=True,
            description='First name of the user'
            ),
        'last_name': fields.String(
            required=True,
            description='Last name of the user'
            ),
        'email': fields.String(
            required=True,
            description='Email of the user',
            pattern=r'^\S+@\S+\.\S+$'
            ),
        'password': fields.String(
            required=True,
            description='Password of the user'
            ),
        })

# Create new user or list users


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered or Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        try:
            new_user = facade.create_user(user_data)
        except ValueError:
            return {'error': 'Invalid input data'}, 400
        return {
            'id': new_user['id'],
            'message': 'User successfully created'
            }, 201

    @api.response(200, 'User list retrieved')
    def get(self):
        """Retrieve all users"""
        users = facade.get_all_users()
        return users, 200

# Retrieve, update, or delete a specific user


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        user.pop('password', None)
        return user, 200

    @jwt_required()
    @api.doc(security='Bearer')
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        token_user_id = get_jwt_identity()
        """Update user details"""
        user_data_to_update = api.payload
        existing_user = facade.get_user_by_email(user_data_to_update["email"])
        if not existing_user:
            return {'error': 'User not found'}, 404
        # check user (from jwt) is accessing only its info
        if not token_user_id == existing_user["id"]:
            return {'message': 'Unauthorized'}, 401
        user = facade.update_user(user_id, user_data_to_update)
        if not user:
            return {'error': 'User not found'}, 404
        return user, 200

    @api.response(200, 'User deleted successfully')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """Delete a user"""
        success = facade.delete_user(user_id)
        if success:
            return {'message': 'User deleted successfully'}, 200
        return {'error': 'User not found'}, 404
