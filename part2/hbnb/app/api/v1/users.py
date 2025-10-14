from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request

usersns = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = usersns.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

@usersns.route('/', methods=['GET', 'POST'])
class UserList(Resource):
    @usersns.expect(user_model, validate=True)
    @usersns.response(201, 'User successfully created')
    @usersns.response(400, 'Email already registered')
    @usersns.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = usersns.payload or {}
        required_fields = ['first_name', 'last_name', 'email']
        for field in required_fields:
            if field not in user_data:
                return {'error': f'Missing required field: {field}'}, 400

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        if existing_user:
            return {'error': 'Email already registered'}, 400
        try:
            new_user = facade.create_user(user_data)
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception:
            return {'error': 'Internal server error'}, 500
        return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email}, 201
    
    def get(self):
        """List all Users"""
        users = facade.get_all_user()
        return [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        } for user in users], 200



@usersns.route('/<user_id>', methods=['GET', 'PUT'])
class UserResource(Resource):
    @usersns.response(200, 'User details retrieved successfully')
    @usersns.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @usersns.expect(user_model, validate=True)
    @usersns.response(200, 'Successfully update')
    @usersns.response(400, 'Invalid input data')
    def put(self, user_id):
        """
        Update an existing user by ID.

        Args:
            user_id (str): Unique identifier of the user.

        Returns:
            tuple: Updated user data dictionary and HTTP 200 on success,
                   or error message and HTTP 404 if not found.
        """
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        data = request.get_json()
        # Update user data and return the updated user
        updated_user = facade.update_user(user_id, data)

        if not updated_user:
            return {'error': 'Update failed'}, 400

        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }
