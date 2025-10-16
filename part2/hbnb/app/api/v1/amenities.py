from flask_restx import Namespace, Resource, fields
from flask import request
from app import facade as facade_instance


amenitiesns = Namespace('amenities', description='Amenity operations')

# Models
amenity_model = amenitiesns.model('AmenityInput', {
    'name': fields.String(required=True, description='Name of the amenity')
})

amenity_response_model = amenitiesns.model('AmenityResponse', {
    'id': fields.String(description='Amenity unique identifier'),
    'name': fields.String(description='Name of the amenity'),
    'created_at': fields.DateTime(dt_format='iso8601'),
    'updated_at': fields.DateTime(dt_format='iso8601')
})

@amenitiesns.route('/')
class AmenityList(Resource):
    @amenitiesns.expect(amenity_model, validate=True)
    @amenitiesns.response(201, 'Amenity successfully created', amenity_response_model)
    def post(self):
        """Create a new Amenity"""
        data = request.get_json()
        try:
            amenity = facade_instance.create_amenity(data)
            return amenity.to_dict(), 201
        except (ValueError, TypeError) as e:
            amenitiesns.abort(400, message=str(e))
        except Exception:
            amenitiesns.abort(500, message='Internal server error')

    @amenitiesns.marshal_list_with(amenity_response_model)
    @amenitiesns.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """List all Amenities"""
        amenities = facade_instance.get_all_amenities()
        return [a.to_dict() for a in amenities]

@amenitiesns.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @amenitiesns.marshal_with(amenity_response_model)
    @amenitiesns.response(200, 'Amenity details retrieved successfully')
    @amenitiesns.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get details for a specific Amenity"""
        amenity = facade_instance.get_amenity(amenity_id)
        if not amenity:
            amenitiesns.abort(404, 'Amenity not found')
        return amenity.to_dict()

    @amenitiesns.expect(amenity_model, validate=True)
    @amenitiesns.marshal_with(amenity_response_model)
    @amenitiesns.response(200, 'Amenity updated successfully')
    @amenitiesns.response(404, 'Amenity not found')
    def put(self, amenity_id):
        """Update a specific Amenity"""
        data = request.get_json()
        try:
            updated = facade_instance.update_amenity(amenity_id, data)
        except (ValueError, TypeError) as e:
            amenitiesns.abort(400, message=str(e))
            
        if not updated:
            amenitiesns.abort(404, 'Amenity not found')
<<<<<<< HEAD
        return updated.to_dict()

    @amenitiesns.response(204, 'Amenity successfully deleted')
    @amenitiesns.response(404, 'Amenity not found')
    def delete(self, amenity_id):
        """Delete a specific Amenity"""
        deleted = facade_instance.delete_amenity(amenity_id)
        if not deleted:
            amenitiesns.abort(404, 'Amenity not found')
        return {"message": "Amenity is deleted"}, 200
=======
        return updated.to_dict(), 200

>>>>>>> d93215b66c691f44bbaebe3e4250ba9e64830dd7
