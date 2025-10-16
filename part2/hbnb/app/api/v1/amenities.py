from flask_restx import Namespace, Resource, fields
from flask import request


amenities_ns = Namespace('amenities', description='Amenity operations')

# Models
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
        data = request.get_json()
        amenity = amenities_ns.facade.create_amenity(data)
        return amenity.to_dict(), 201

    @amenities_ns.marshal_list_with(amenity_response_model)
    @amenities_ns.response(200, 'List of amenities retrieved successfully')
    def get(self):
        amenities = amenities_ns.facade.get_all_amenities()
        return [a.to_dict() for a in amenities], 200

@amenities_ns.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @amenities_ns.marshal_with(amenity_response_model)
    @amenities_ns.response(200, 'Amenity details retrieved successfully')
    @amenities_ns.response(404, 'Amenity not found')
    def get(self, amenity_id):
        amenity = amenities_ns.facade.get_amenity(amenity_id)
        if not amenity:
            amenities_ns.abort(404, 'Amenity not found')
        return amenity.to_dict(), 200

    @amenities_ns.expect(amenity_model, validate=True)
    @amenities_ns.response(200, 'Amenity updated successfully')
    @amenities_ns.response(404, 'Amenity not found')
    def put(self, amenity_id):
        data = request.get_json()
        updated = amenities_ns.facade.update_amenity(amenity_id, data)
        if not updated:
            amenities_ns.abort(404, 'Amenity not found')
        return updated.to_dict(), 200

