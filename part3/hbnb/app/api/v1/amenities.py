from flask_restx import Namespace, Resource, fields
from flask import request
from app import facade as facade_instance
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

amenities_ns = Namespace('amenities', description='Amenity operations')


# -----------------------
# Models for Swagger
# -----------------------
amenity_model = amenities_ns.model('AmenityInput', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'place_id': fields.String(required=True, description='ID of the place this amenity belongs to')
})

amenity_response_model = amenities_ns.model('AmenityResponse', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity'),
    'place_id': fields.String(description='ID of the place this amenity belongs to'),
    'owner_id': fields.String(description='ID of the place owner who created the amenity'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})


# -----------------------
# Routes
# -----------------------
@amenities_ns.route('/')
class AmenityList(Resource):
    
    @jwt_required()  # Protected: Place owner or admin can create amenities
    @amenities_ns.expect(amenity_model, validate=True)
    @amenities_ns.response(201, 'Amenity successfully created', amenity_response_model)
    @amenities_ns.response(400, 'Invalid input data')
    @amenities_ns.response(403, 'Unauthorized action')
    @amenities_ns.response(404, 'Place not found')
    def post(self):
        """Register a new amenity for a place (Protected - place owner or admin only)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        try:
            amenity_data = amenities_ns.payload
            place_id = amenity_data.get('place_id')
            
            # Get the place to verify ownership
            place = facade_instance.get_place(place_id)
            if not place:
                amenities_ns.abort(404, 'Place not found')
            
            # Check if user is the place owner or admin
            if place.owner_id != current_user_id and not is_admin:
                amenities_ns.abort(403, 'You can only add amenities to your own places')
            
            # Add the owner_id (place owner)
            amenity_data['owner_id'] = place.owner_id
            
            new_amenity = facade_instance.create_amenity(amenity_data)
            return new_amenity.to_dict(), 201
            
        except ValueError as e:
            amenities_ns.abort(400, str(e))
        except Exception as e:
            amenities_ns.abort(500, f"Internal error: {str(e)}")

    @amenities_ns.marshal_list_with(amenity_response_model)
    @amenities_ns.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities (Public endpoint)"""
        amenities = facade_instance.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities]


@amenities_ns.route('/<string:amenity_id>')
@amenities_ns.param('amenity_id', 'The Amenity identifier (UUID)')
class AmenityResource(Resource):
    
    @amenities_ns.marshal_with(amenity_response_model)
    @amenities_ns.response(200, 'Amenity details retrieved successfully')
    @amenities_ns.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID (Public endpoint)"""
        amenity = facade_instance.get_amenity(amenity_id)
        if not amenity:
            amenities_ns.abort(404, 'Amenity not found')
        return amenity.to_dict()

    @jwt_required()  # Protected: Place owner or admin
    @amenities_ns.expect(amenity_model, validate=True)
    @amenities_ns.marshal_with(amenity_response_model)
    @amenities_ns.response(200, 'Amenity updated successfully')
    @amenities_ns.response(404, 'Amenity not found')
    @amenities_ns.response(400, 'Invalid input data')
    @amenities_ns.response(403, 'Unauthorized action')
    def put(self, amenity_id):
        """Update an amenity (Protected - place owner or admin only)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        # Get the amenity to check ownership
        amenity = facade_instance.get_amenity(amenity_id)
        if not amenity:
            amenities_ns.abort(404, 'Amenity not found')
        
        # Check if user is place owner or admin
        if amenity.owner_id != current_user_id and not is_admin:
            amenities_ns.abort(403, 'You can only update amenities of your own places')
        
        try:
            amenity_data = amenities_ns.payload
            
            # If place_id is being changed, verify ownership of the new place too
            if 'place_id' in amenity_data:
                new_place_id = amenity_data['place_id']
                new_place = facade_instance.get_place(new_place_id)
                if not new_place:
                    amenities_ns.abort(404, 'New place not found')
                
                if new_place.owner_id != current_user_id and not is_admin:
                    amenities_ns.abort(403, 'You can only move amenities to your own places')
            
            updated_amenity = facade_instance.update_amenity(amenity_id, amenity_data)
            
            if not updated_amenity:
                amenities_ns.abort(404, 'Amenity not found')
            
            return updated_amenity.to_dict()
            
        except ValueError as e:
            amenities_ns.abort(400, str(e))
        except Exception as e:
            amenities_ns.abort(500, f"Internal error: {str(e)}")

    @jwt_required()  # Protected: Place owner or admin
    @amenities_ns.response(204, 'Amenity deleted successfully')
    @amenities_ns.response(404, 'Amenity not found')
    @amenities_ns.response(403, 'Unauthorized action')
    def delete(self, amenity_id):
        """Delete an amenity (Protected - place owner or admin only)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        # Get the amenity to check ownership
        amenity = facade_instance.get_amenity(amenity_id)
        if not amenity:
            amenities_ns.abort(404, 'Amenity not found')
        
        # Check if user is place owner or admin
        if amenity.owner_id != current_user_id and not is_admin:
            amenities_ns.abort(403, 'You can only delete amenities of your own places')
        
        if facade_instance.delete_amenity(amenity_id):
            return {}, 204
        amenities_ns.abort(404, 'Amenity not found')