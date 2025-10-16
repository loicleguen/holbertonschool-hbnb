from flask_restx import Namespace, Resource, fields
from flask import request
from app import facade as facade_instance


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

place_update_model = placesns.model('PlaceUpdateInput', {
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
    @placesns.expect(place_model, validate=True)
    @placesns.response(201, 'Place registered successfully', place_response)
    def post(self):
        """Register a new place"""
        try:
            place_data = request.get_json()
            place = facade_instance.create_place(place_data)
            
            # --- FIX: Populate 'owner' field in the response ---
            # Fetch the owner object and pass it to to_dict
            owner_obj = facade_instance.get_user(place.owner_id)
            
            return place.to_dict(owners_map={place.owner_id: owner_obj}), 201
            # --- END FIX ---
            
        except ValueError as e:
            places_ns.abort(400, str(e))
        except Exception as e:
            places_ns.abort(500, f"Internal error: {str(e)}")


    @placesns.marshal_list_with(place_response)
    @placesns.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve all places with optimized owner and amenities fetching"""
        places = facade_instance.get_all_places()

        # Gather all unique owner IDs and amenity IDs
        owner_ids = {p.owner_id for p in places if p.owner_id}
        amenity_ids = {amenity_obj.id for p in places for amenity_obj in p.amenities if hasattr(amenity_obj, 'id')}

        # Fetch objects in batch using Facade helper methods
        owners = {user.id: user for user in facade_instance.get_users_by_ids(list(owner_ids))}
        amenities = {a.id: a for a in facade_instance.get_amenities_by_ids(list(amenity_ids))}

        # Build the response using to_dict with maps
        result = [p.to_dict(owners_map=owners, amenities_map=amenities) for p in places]

        return result


@places_ns.route('/<string:place_id>')
@places_ns.param('place_id', 'The place unique identifier')
class PlaceResource(Resource):
    @placesns.marshal_with(place_response)
    @placesns.response(404, 'Place not found')
    @placesns.response(200, 'Place details retrieved successfully')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade_instance.get_place(place_id)
        if not place:
            placesns.abort(404, 'Place not found')

        # Retrieve the owner and amenities for serialization
        owner_obj = facade_instance.get_user(place.owner_id)
        # Assuming the Place object stores the Amenity objects (as set in Facade)
        # We still fetch all amenities to be robust.
        amenity_ids = {a.id for a in place.amenities if hasattr(a, 'id')}
        amenities_map = {a.id: a for a in facade_instance.get_amenities_by_ids(list(amenity_ids))}

        # Use to_dict with the required maps
        return place.to_dict(
            owners_map={place.owner_id: owner_obj} if owner_obj else None, 
            amenities_map=amenities_map
        )

    @placesns.expect(place_update_model, validate=True)
    @placesns.response(200, 'Place updated successfully', place_response)
    @placesns.response(404, 'Place not found')
    @placesns.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place"""
        try:
            place_data = request.get_json()
            updated_place = facade_instance.update_place(place_id, place_data)
            if not updated_place:
                placesns.abort(404, "Place not found")
            
            # --- FIX: Populate 'owner' field in the response ---
            # Fetch the owner object to correctly serialize the 'owner' field in to_dict
            owner_obj = facade_instance.get_user(updated_place.owner_id)
            
            amenity_ids = {a.id for a in updated_place.amenities if hasattr(a, 'id')}
            amenities_map = {a.id: a for a in facade_instance.get_amenities_by_ids(list(amenity_ids))}

            # Call to_dict with the required maps
            return updated_place.to_dict(
                owners_map={updated_place.owner_id: owner_obj},
                amenities_map=amenities_map
            )
            # --- END FIX ---
            
        except ValueError as e:
            places_ns.abort(400, str(e))
        except Exception as e:
            placesns.abort(500, f"Internal error: {str(e)}")

    @placesns.response(204, 'Place successfully deleted')
    @placesns.response(404, 'Place not found')
    def delete(self, place_id):
        """Delete a place by ID"""
        deleted = facade_instance.delete_place(place_id)
        if not deleted:
            placesns.abort(404, 'Place not found')
        return {"message": "Place is deleted"}, 200
