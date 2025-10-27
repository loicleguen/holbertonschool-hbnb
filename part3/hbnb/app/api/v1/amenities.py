from flask_restx import Namespace, Resource, fields
from flask import request
from app import facade as facade_instance


amenities_ns = Namespace('amenities', description='Amenity operations')

amenity_model = amenities_ns.model('AmenityInput', {
    'name': fields.String(required=True, description='Name of the amenity')
})

amenity_response_model = amenities_ns.model('AmenityResponse', {
    'id': fields.String(description='Amenity unique identifier'),
    'name': fields.String(description='Name of the amenity'),
    'created_at': fields.DateTime(dt_format='iso8601'),
    'updated_at': fields.DateTime(dt_format='iso8601')
})

@amenities_ns.route('/')
class AmenityList(Resource):
    @amenities_ns.expect(amenity_model, validate=True)
    @amenities_ns.response(201, 'Amenity successfully created', amenity_response_model)
    def post(self):
        """Create a new Amenity"""
        data = request.get_json()
        try:
            amenity = facade_instance.create_amenity(data)
            return amenity.to_dict(), 201
        except (ValueError, TypeError) as e:
            amenities_ns.abort(400, message=str(e))
        except Exception:
            amenities_ns.abort(500, message='Internal server error')

    @amenities_ns.marshal_list_with(amenity_response_model)
    @amenities_ns.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """List all Amenities"""
        amenities = facade_instance.get_all_amenities()
        return [a.to_dict() for a in amenities]

@amenities_ns.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @amenities_ns.marshal_with(amenity_response_model)
    @amenities_ns.response(200, 'Amenity details retrieved successfully')
    @amenities_ns.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get details for a specific Amenity"""
        amenity = facade_instance.get_amenity(amenity_id)
        if not amenity:
            amenities_ns.abort(404, 'Amenity not found')
        return amenity.to_dict()

    @amenities_ns.expect(amenity_model, validate=True)
    @amenities_ns.marshal_with(amenity_response_model)
    @amenities_ns.response(200, 'Amenity updated successfully')
    @amenities_ns.response(404, 'Amenity not found')
    def put(self, amenity_id):
        """Update a specific Amenity"""
        data = request.get_json()
        
        try:
            updated = facade_instance.update_amenity(amenity_id, data)
        except (ValueError, TypeError) as e:
            amenities_ns.abort(400, message=str(e))
            
        if not updated:
            amenities_ns.abort(404, 'Amenity not found')
        return updated.to_dict()

    @amenities_ns.response(204, 'Amenity successfully deleted')
    @amenities_ns.response(404, 'Amenity not found')
    def delete(self, amenity_id):
        """Delete a specific Amenity"""
        deleted = facade_instance.delete_amenity(amenity_id)
        if not deleted:
            amenities_ns.abort(404, 'Amenity not found')
        return {}, 204
