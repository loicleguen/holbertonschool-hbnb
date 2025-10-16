from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from flask import request


# Initialisation du namespace
placesns = Namespace('places', description='Place operations')


# -----------------------
# Models for Swagger
# -----------------------
amenity_model = placesns.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = placesns.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

place_model = placesns.model('PlaceInput', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, description="List of amenity IDs")
})

place_response = placesns.model('PlaceResponse', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude'),
    'longitude': fields.Float(description='Longitude'),
    'owner': fields.Nested(user_model),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp'),
    'amenities': fields.List(fields.Nested(amenity_model))
})

# -----------------------
# Routes
# -----------------------
@placesns.route('/')
class PlaceList(Resource):
    @placesns.expect(place_model, validate=True)
    def post(self):
        """Register a new place"""
        try:
            place_data = request.get_json()
            place = placesns.facade.create_place(place_data)
            return place.to_dict(), 201
        except ValueError as e:
            placesns.abort(400, str(e))
        except Exception as e:
            placesns.abort(500, f"Internal error: {str(e)}")


    @placesns.marshal_list_with(place_response)
    def get(self):
        """Retrieve all places"""
        places = placesns.facade.get_all_places()
        return [placesns.facade.get_place(p.id) for p in places], 200


@placesns.route('/<string:place_id>')
@placesns.param('place_id', 'The place unique identifier')
class PlaceResource(Resource):
    @placesns.marshal_with(place_response)
    @placesns.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = placesns.facade.get_place(place_id)
        if not place:
            placesns.abort(404, 'Place not found')
        return place, 200

    @placesns.expect(place_model, validate=True)
    def put(self, place_id):
        """Update a place"""
        try:
            updated = placesns.facade.update_place(place_id, placesns.payload)
            if not updated:
                placesns.abort(404, 'Place not found')
            return {"message": "Place updated successfully"}, 200
        except ValueError as e:
            placesns.abort(400, str(e))
        except Exception as e:
            placesns.abort(500, f"Internal error: {str(e)}")
