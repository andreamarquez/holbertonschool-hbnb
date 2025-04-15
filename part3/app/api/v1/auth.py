from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from app.services import facade


api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})


@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.response(200, 'Successfully authenticated')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Authenticate user and return a JWT token"""
        # Get the email and password from the request payload
        credentials = api.payload

        # Check if the user exists and the password is correct
        user = facade.get_verified_user(
            credentials['email'],
            credentials['password'])

        # if the user does not exist or the password is wrong
        if not user:
            return {'error': 'Invalid credentials'}, 401

        # Create a JWT token with the user's id and is_admin flag
        access_token = create_access_token(
            identity=str(user.id),  # Use the user ID as the identity
            additional_claims={
                'is_admin': user.is_admin,
                'email': user.email
                }  # Add extra data
        )
        # Return the JWT token to the client
        return {'access_token': access_token}, 200


@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    @api.doc(security='Bearer')
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        # Retrieve the user's identity
        # from the token
        user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', None)
        email = claims.get('email', None)

        return {
            'message': f'Hello, user {user_id}',
            'is_admin': is_admin,
            'email': email
        }, 200
