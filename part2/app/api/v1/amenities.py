from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
})


@api.route('/')
class AmenityList(Resource):
    """
    Handles the creation and retrieval of amenities.
    """

    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Register a new amenity.
        Handles the POST request to create a new amenity.
        """
        amenity_data = api.payload

        try:
            new_amenity = facade.create_amenity(amenity_data)
        except ValueError:
            return {'error': 'Invalid input data'}, 400

        return new_amenity, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """
        Retrieve a list of all amenities.
        Handles the GET request to fetch all available amenities.
        """
        amenities = facade.get_all_amenities()

        if not amenities:
            return {'error': 'No amenities found'}, 404

        return amenities, 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    """
    Handles operations on a specific amenity identified by amenity_id.
    """
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """
        Get amenity details by ID.
        """
        amenity = facade.get_amenity(amenity_id)

        if not amenity:
            return {'error': 'Amenity not found'}, 404

        return amenity, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """
        Update an amenity's information.
        Handles the PUT request to update an amenity's data.
        """
        amenity_data = api.payload

        if not amenity_data:
            return {'message': 'Invalid input data'}, 400

        updated_amenity = facade.update_amenity(amenity_id, amenity_data)

        if not updated_amenity:
            return {'error': 'Amenity not found'}, 404

        return updated_amenity, 200

    @api.response(200, 'Amenity successfully deleted')
    @api.response(404, 'Amenity not found')
    def delete(self, amenity_id):
        """
        Delete an amenity.
        Handles the DELETE request to remove an amenity by its ID.
        """
        success = facade.delete_amenity(amenity_id)

        if success:
            return {'message': 'Amenity deleted successfully'}, 200
        else:
            return {'error': 'Amenity not found'}, 404
