from flask_restx import Namespace, Resource, fields
from flask import request
from app import facade as facade_instance


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
    @places_ns.expect(place_model, validate=True)
    @places_ns.marshal_with(place_response, code=201)
    @places_ns.response(400, 'Invalid input data')
    @places_ns.response(404, 'Owner not found')
    def post(self):
        """Create a new Place"""
        data = places_ns.payload
        owner_id = data.get('owner_id')

        if not facade_instance.get_user(owner_id):
            places_ns.abort(404, 'Owner not found')

        try:
            new_place = facade_instance.create_place(data)
            return new_place.to_dict(users_map={owner_id: facade_instance.get_user(owner_id)}), 201
        except ValueError as e:
            places_ns.abort(400, str(e))
        except Exception as e:
             places_ns.abort(500, f"Internal Server Error: {str(e)}")


    @places_ns.marshal_list_with(place_response)
    @places_ns.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve all places with optimized owner and amenities fetching"""
        places = facade_instance.get_all_places()

        owner_ids = {p.owner_id for p in places if p.owner_id}
        amenity_ids = {amenity_obj.id for p in places for amenity_obj in p.amenities if hasattr(amenity_obj, 'id')}

        owners = {user.id: user for user in facade_instance.get_users_by_ids(list(owner_ids))}
        amenities = {a.id: a for a in facade_instance.get_amenities_by_ids(list(amenity_ids))}

        result = [p.to_dict(owners_map=owners, amenities_map=amenities) for p in places]

        return result


@places_ns.route('/<string:place_id>')
@places_ns.param('place_id', 'The place unique identifier')
class PlaceResource(Resource):
    @places_ns.marshal_with(place_response)
    @places_ns.response(404, 'Place not found')
    @places_ns.response(200, 'Place details retrieved successfully')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade_instance.get_place(place_id)
        if not place:
            places_ns.abort(404, 'Place not found')

        owner_obj = facade_instance.get_user(place.owner_id)

        amenity_ids = {a.id for a in place.amenities if hasattr(a, 'id')}
        amenities_map = {a.id: a for a in facade_instance.get_amenities_by_ids(list(amenity_ids))}


        return place.to_dict(
            owners_map={place.owner_id: owner_obj} if owner_obj else None, 
            amenities_map=amenities_map
        )

    @places_ns.expect(place_update_model, validate=True)
    @places_ns.response(200, 'Place updated successfully', place_response)
    @places_ns.response(404, 'Place not found')
    @places_ns.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place"""
        try:
            place_data = request.get_json()
            updated_place = facade_instance.update_place(place_id, place_data)
            if not updated_place:
                places_ns.abort(404, "Place not found")

            owner_obj = facade_instance.get_user(updated_place.owner_id)
            
            amenity_ids = {a.id for a in updated_place.amenities if hasattr(a, 'id')}
            amenities_map = {a.id: a for a in facade_instance.get_amenities_by_ids(list(amenity_ids))}


            return updated_place.to_dict(
                owners_map={updated_place.owner_id: owner_obj},
                amenities_map=amenities_map
            )
            
        except ValueError as e:
            places_ns.abort(400, str(e))
        except Exception as e:
            places_ns.abort(500, f"Internal error: {str(e)}")

    @places_ns.response(204, 'Place successfully deleted')
    @places_ns.response(404, 'Place not found')
    def delete(self, place_id):
        """Delete a place by ID"""
        deleted = facade_instance.delete_place(place_id)
        if not deleted:
            places_ns.abort(404, 'Place not found')
        return {}, 204