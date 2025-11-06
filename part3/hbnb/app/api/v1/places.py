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
    @jwt_required()  # 🔒 PROTECTED: User must be authenticated to create a place
    @places_ns.expect(place_model, validate=True)
    @places_ns.response(201, 'Place registered successfully', place_response)
    @places_ns.response(400, 'Invalid input data')
    @places_ns.response(403, 'Unauthorized action')
    def post(self):
        """Register a new place (Protected - authentication required)"""
 
        try:
            place_data = places_ns.payload

            current_user_id = get_jwt_identity()

            place_data['owner_id'] = current_user_id
            
            # Verify that the owner_id matches the authenticated user
            if 'owner_id' in places_ns.payload and places_ns.payload['owner_id'] != current_user_id:
                places_ns.abort(403, 'Cannot set owner_id to another user')
            
            place = facade_instance.create_place(place_data)

            owner_obj = facade_instance.get_user(place.owner_id)
            
            # Build amenities map (place.amenities contains objects)
            amenities_map = {a.id: a for a in place.amenities}

            # Build reviews map (empty on creation)
            reviews_map = facade_instance.get_reviews_by_place(place.id)

            return place.to_dict(
                owners_map={place.owner_id: owner_obj} if owner_obj else None,
                amenities_map=amenities_map,
                reviews_map=reviews_map
            ), 201
            
        except ValueError as e:
            places_ns.abort(400, str(e))
        except Exception as e:
            places_ns.abort(500, f"Internal error: {str(e)}")


    @places_ns.marshal_list_with(place_response)
    @places_ns.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve all places with owner, amenities, and reviews (Public)"""
        places = facade_instance.get_all_places()

        # Owners map
        owners = {u.id: u for u in facade_instance.get_all_user()}

        result = []
        for p in places:
            # Amenities map
            amenities_map = {a.id: a for a in p.amenities}

            # Reviews map
            reviews_map = facade_instance.get_reviews_by_place(p.id)

            result.append(p.to_dict(
                owners_map={p.owner_id: owners.get(p.owner_id)},
                amenities_map=amenities_map,
                reviews_map=reviews_map
            ))

        return result


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

        owner_obj = facade_instance.get_user(place.owner_id)
        amenities_map = {a.id: a for a in place.amenities}
        reviews_map = facade_instance.get_reviews_by_place(place.id)

        return place.to_dict(
            owners_map={place.owner_id: owner_obj} if owner_obj else None, 
            amenities_map=amenities_map,
            reviews_map=reviews_map
        )

    @jwt_required()  # 🔒 PROTECTED: Owner or admin only
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

            owner_obj = facade_instance.get_user(updated_place.owner_id)
            amenities_map = {a.id: a for a in updated_place.amenities}
            reviews_map = facade_instance.get_reviews_by_place(updated_place.id)

            return updated_place.to_dict(
                owners_map={updated_place.owner_id: owner_obj},
                amenities_map=amenities_map,
                reviews_map=reviews_map
            )
            
        except ValueError as e:
            places_ns.abort(400, str(e))
        except Exception as e:
            places_ns.abort(500, f"Internal error: {str(e)}")

    @jwt_required()  # 🔒 PROTECTED: Owner or admin only
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
        return {}, 204