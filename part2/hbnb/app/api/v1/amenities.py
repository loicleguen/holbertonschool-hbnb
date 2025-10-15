from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

# Initialize Facade instance
facade = HBnBFacade()

# Define Namespace and Models
amenities_ns = Namespace('amenities', description='Amenity operations')

# Model for POST/PUT input data
amenity_model = amenities_ns.model('AmenityInput', {
    'name': fields.String(required=True, description='Name of the amenity')
})

# Model for GET response data
amenity_response_model = amenities_ns.model('AmenityResponse', {
    'id': fields.String(description='Amenity unique identifier'),
    'name': fields.String(description='Name of the amenity'),
    'created_at': fields.DateTime(dt_format='iso8601'),
    'updated_at': fields.DateTime(dt_format='iso8601'),
})

@amenities_ns.route('/')
class AmenityList(Resource):
    @amenities_ns.doc('create_amenity')
    @amenities_ns.expect(amenity_model, validate=True)
    @amenities_ns.response(201, 'Amenity successfully created', amenity_response_model)
    @amenities_ns.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        try:
            amenity = facade.create_amenity(amenities_ns.payload)
            return amenity.to_dict(), 201
        except ValueError as e:
            amenities_ns.abort(400, str(e))
        except Exception as e:
            amenities_ns.abort(500, "An internal error occurred: " + str(e))

    @amenities_ns.doc('list_amenities')
    @amenities_ns.marshal_list_with(amenity_response_model)
    @amenities_ns.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200


@amenities_ns.route('/<string:amenity_id>')
@amenities_ns.param('amenity_id', 'The Amenity identifier (UUID)')
class AmenityResource(Resource):
    @amenities_ns.doc('get_amenity')
    @amenities_ns.marshal_with(amenity_response_model)
    @amenities_ns.response(200, 'Amenity details retrieved successfully')
    @amenities_ns.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            amenities_ns.abort(404, 'Amenity not found')
        return amenity.to_dict(), 200

    @amenities_ns.doc('update_amenity')
    @amenities_ns.expect(amenity_model, validate=True)
    @amenities_ns.response(200, 'Amenity updated successfully') 
    @amenities_ns.response(404, 'Amenity not found')
    @amenities_ns.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        
        if not facade.get_amenity(amenity_id):
            amenities_ns.abort(404, 'Amenity not found')

        try:
            updated_amenity = facade.update_amenity(amenity_id, amenities_ns.payload)
            
            if not updated_amenity:
                amenities_ns.abort(404, 'Amenity not found') 
            
            return {"message": "Amenity updated successfully"}, 200
        except ValueError as e:
            amenities_ns.abort(400, str(e))
        except Exception as e:
            amenities_ns.abort(500, "An internal error occurred: " + str(e))
