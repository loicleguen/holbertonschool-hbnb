from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import HBnBFacade

facade = HBnBFacade()
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
        data = request.get_json()
        amenity = facade.create_amenity(data)
        return amenity.to_dict(), 201

    @amenitiesns.marshal_list_with(amenity_response_model)
    @amenitiesns.response(200, 'List of amenities retrieved successfully')
    def get(self):
        amenities = facade.get_all_amenities()
        return [a.to_dict() for a in amenities], 200

@amenitiesns.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @amenitiesns.marshal_with(amenity_response_model)
    @amenitiesns.response(200, 'Amenity details retrieved successfully')
    @amenitiesns.response(404, 'Amenity not found')
    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            amenitiesns.abort(404, 'Amenity not found')
        return amenity.to_dict(), 200

    @amenitiesns.expect(amenity_model, validate=True)
    @amenitiesns.response(200, 'Amenity updated successfully')
    @amenitiesns.response(404, 'Amenity not found')
    def put(self, amenity_id):
        data = request.get_json()
        updated = facade.update_amenity(amenity_id, data)
        if not updated:
            amenitiesns.abort(404, 'Amenity not found')
        return updated.to_dict(), 200
