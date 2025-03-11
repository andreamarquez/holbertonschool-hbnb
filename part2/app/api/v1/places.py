from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Amenity name')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='Owner\'s first name'),
    'last_name': fields.String(description='Owner\'s last name'),
    'email': fields.String(description='Owner\'s email')
})

# new review model
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# update of place modele for including reviews
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude'),
    'owner_id': fields.String(required=True, description='Owner ID'),
    'amenities': fields.List(fields.String, required=True, description="Amenities IDs"),
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place created')
    @api.response(400, 'Invalid data')
    def post(self):
        """Create a new place"""
        place_data = api.payload
        if not place_data:
            return {'message': 'Invalid data'}, 400
        new_place = facade.create_place(place_data)
        return new_place, 201

    @api.response(200, 'Places list')
    def get(self):
        """Retrieve all places"""
        places = facade.get_all_places()
        return places, 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Retrieve a place's details, including its reviews"""
        place = facade.get_place(place_id)
        if not place:
            return {'message': 'Not found'}, 404
        
        # retrieve reviews associated with the location
        reviews = facade.get_reviews_by_place(place_id)
        place['reviews'] = reviews
        return place, 200

    @api.response(200, 'Place deleted')
    @api.response(404, 'Place not found')
    def delete(self, place_id):
        """Delete a place"""
        success = facade.delete_place(place_id)
        if success:
            return {'message': 'Deleted'}, 200
        return {'message': 'Not found'}, 404

    @api.expect(place_model)
    @api.response(200, 'Place updated')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid data')
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload
        if not place_data:
            return {'message': 'Invalid data'}, 400
        updated_place = facade.update_place(place_id, place_data)
        if not updated_place:
            return {'message': 'Not found'}, 404
        return updated_place, 200
    