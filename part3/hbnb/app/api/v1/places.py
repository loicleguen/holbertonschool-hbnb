from flask_restx import Namespace, Resource, fields
from flask import request
from app import facade as facade_instance
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


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

place_update_model = places_ns.model('PlaceUpdateInput', {
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
})

# -----------------------
# Routes
# -----------------------
@places_ns.route('/')
class PlaceList(Resource):
    @jwt_required()
    @places_ns.expect(place_model, validate=True)
    @places_ns.response(201, 'Place registered successfully', place_response)
    @places_ns.response(400, 'Invalid input data')
    @places_ns.response(403, 'Unauthorized action')
    def post(self):
        """Register a new place (Protected - authentication required)"""
        current_user_id = get_jwt_identity()
        
        try:
            place_data = request.get_json()
            
            # Verify that the owner_id matches the authenticated user
            if place_data.get('owner_id') != current_user_id:
                places_ns.abort(403, 'You can only create places for yourself')
            
            place = facade_instance.create_place(place_data)
            
            # ✅ SQLAlchemy charge automatiquement owner, amenities, reviews
            return place.to_dict(), 201
            
        except ValueError as e:
            places_ns.abort(400, str(e))
        except Exception as e:
            places_ns.abort(500, f"Internal error: {str(e)}")


    @places_ns.marshal_list_with(place_response)
    @places_ns.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve all places with owner, amenities, and reviews (Public)"""
        places = facade_instance.get_all_places()
        
        # ✅ SQLAlchemy charge automatiquement toutes les relations
        return [p.to_dict() for p in places]


@places_ns.route('/<string:place_id>')
@places_ns.param('place_id', 'The place unique identifier')
class PlaceResource(Resource):
    @places_ns.marshal_with(place_response)
    @places_ns.response(404, 'Place not found')
    @places_ns.response(200, 'Place details retrieved successfully')
    def get(self, place_id):
        """Get place details by ID (Public)"""
        place = facade_instance.get_place(place_id)
        if not place:
            places_ns.abort(404, 'Place not found')

        # ✅ SQLAlchemy charge automatiquement owner, amenities, reviews
        return place.to_dict()

    @jwt_required()
    @places_ns.expect(place_update_model, validate=True)
    @places_ns.response(200, 'Place updated successfully', place_response)
    @places_ns.response(404, 'Place not found')
    @places_ns.response(400, 'Invalid input data')
    @places_ns.response(403, 'Unauthorized action')
    def put(self, place_id):
        """Update a place (Protected - owner or admin only)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        # Get the place to check ownership
        place = facade_instance.get_place(place_id)
        if not place:
            places_ns.abort(404, "Place not found")
        
        # Check if user is owner or admin
        if place.owner_id != current_user_id and not is_admin:
            places_ns.abort(403, 'You can only update your own places')
        
        try:
            place_data = request.get_json()
            updated_place = facade_instance.update_place(place_id, place_data)
            
            # ✅ SQLAlchemy charge automatiquement owner, amenities, reviews
            return updated_place.to_dict()
            
        except ValueError as e:
            places_ns.abort(400, str(e))
        except Exception as e:
            places_ns.abort(500, f"Internal error: {str(e)}")

    @jwt_required()
    @places_ns.response(204, 'Place successfully deleted')
    @places_ns.response(404, 'Place not found')
    @places_ns.response(403, 'Unauthorized action')
    def delete(self, place_id):
        """Delete a place by ID (Protected - owner or admin only)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        # Get the place to check ownership
        place = facade_instance.get_place(place_id)
        if not place:
            places_ns.abort(404, 'Place not found')
        
        # Check if user is owner or admin
        if place.owner_id != current_user_id and not is_admin:
            places_ns.abort(403, 'You can only delete your own places')
        
        facade_instance.delete_place(place_id)

        return {"message": "Place successfully deleted"}, 204