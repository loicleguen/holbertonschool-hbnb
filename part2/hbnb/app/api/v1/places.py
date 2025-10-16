from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from flask import request


# Initialisation du namespace
places_ns = Namespace('places', description='Place operations')


# -----------------------
# Models for Swagger
# -----------------------
amenity_model = places_ns.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = places_ns.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_display_model = places_ns.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

place_model = places_ns.model('PlaceInput', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, description="List of amenity IDs")
})

place_response = places_ns.model('PlaceResponse', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude'),
    'longitude': fields.Float(description='Longitude'),
    'owner': fields.Nested(user_model),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp'),
    'amenities': fields.List(fields.Nested(amenity_model)),
    'reviews': fields.List(fields.Nested(review_display_model), description='List of reviews') 
})

# -----------------------
# Routes
# -----------------------
@places_ns.route('/')
class PlaceList(Resource):
    @places_ns.expect(place_model, validate=True)
    def post(self):
        """Register a new place"""
        try:
            place_data = request.get_json()
            place = places_ns.facade.create_place(place_data)
            return place.to_dict(), 201
        except ValueError as e:
            places_ns.abort(400, str(e))
        except Exception as e:
            places_ns.abort(500, f"Internal error: {str(e)}")


    @places_ns.marshal_list_with(place_response)
    def get(self):
        """Retrieve all places"""
        places = places_ns.facade.get_all_places()
        return [places_ns.facade.get_place(p.id) for p in places], 200


@places_ns.route('/<string:place_id>')
@places_ns.param('place_id', 'The place unique identifier')
class PlaceResource(Resource):
    @places_ns.marshal_with(place_response)
    @places_ns.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = places_ns.facade.get_place(place_id)
        if not place:
            places_ns.abort(404, 'Place not found')
        return place, 200

    @places_ns.expect(place_model, validate=True)
    def put(self, place_id):
        """Update a place"""
        try:
            updated = places_ns.facade.update_place(place_id, places_ns.payload)
            if not updated:
                places_ns.abort(404, 'Place not found')
            return {"message": "Place updated successfully"}, 200
        except ValueError as e:
            places_ns.abort(400, str(e))
        except Exception as e:
            places_ns.abort(500, f"Internal error: {str(e)}")
