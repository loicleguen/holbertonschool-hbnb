from flask_restx import Namespace, Resource, fields
from flask import request
from app import facade as facade_instance
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


users_ns = Namespace('users', description='User operations')

user_model = users_ns.model('UserInput', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
})

# User model for API Response
user_response_model = users_ns.model('UserResponse', {
    'id': fields.String(description='User unique identifier'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'is_admin': fields.Boolean(description='Administrative rights flag (default: False)', default=False),
    'created_at': fields.String(description='The timestamp of creation'),
    'updated_at': fields.String(description='The timestamp of last update')
})

# Model for user update (PUT)
user_update_model = users_ns.model('UserUpdateInput', {
    'first_name': fields.String(required=False, description='First name of the user'),
    'last_name': fields.String(required=False, description='Last name of the user'),
    'email': fields.String(required=True, is_admin=True, description='Email of the user'),
    'password': fields.String(required=True, is_admin=True, description='Password of the user'),
})


# ---------------------------
# User list and creation
# ---------------------------
@users_ns.route('/')
class UserList(Resource):

    @jwt_required()
    @users_ns.expect(user_model, validate=True)
    @users_ns.response(201, 'User successfully created', user_response_model)
    @users_ns.response(400, 'Email already registered or invalid input')
    @users_ns.response(403, 'Unauthorized action')
    @users_ns.response(500, 'Internal server error')
    def post(self):
        """Register a new user"""
        user_data = request.get_json() or {}
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        if not is_admin: # <--- MODIFICATION: Admin check
            users_ns.abort(403, 'Admin privilege required to create new users')

        try:
            new_user = facade_instance.create_user(user_data)
        except (ValueError, TypeError) as e:
            users_ns.abort(400, message=str(e))
        except Exception:
            users_ns.abort(500, message='Internal server error')

        return new_user.to_dict(), 201

    @users_ns.marshal_list_with(user_response_model)
    @users_ns.response(200, 'List of users retrieved successfully')
    def get(self):
        """List all users"""
        users = facade_instance.get_all_user()
        return [u.to_dict() for u in users]


# ---------------------------
# User details and update/delete
# ---------------------------
@users_ns.route('/<string:user_id>')
class UserResource(Resource):

    @jwt_required()
    @users_ns.marshal_with(user_response_model)
    @users_ns.response(200, 'User details retrieved successfully')
    @users_ns.response(403, 'Unauthorized action')
    @users_ns.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID (Self or Admin only)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        if user_id != current_user_id and not is_admin:
            users_ns.abort(403, 'You can only view your own profile or must be an admin')

    @jwt_required()  # Protected: Users can update their profile, admins can update any user
    @users_ns.expect(user_update_model, validate=True)
    @users_ns.marshal_with(user_response_model) 
    @users_ns.response(200, 'User successfully updated')
    @users_ns.response(400, 'Invalid input data')
    @users_ns.response(403, 'Unauthorized action')
    @users_ns.response(404, 'User not found')
    def put(self, user_id):
        """Update a user's details (Self or Admin only)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        user_data = users_ns.payload

        # Check authorization
        if user_id != current_user_id and not is_admin:
            users_ns.abort(403, 'You can only update your own profile or must be an admin')

        # Regular user restrictions
        if not is_admin and user_id == current_user_id:
            if 'is_admin' in user_data:
                users_ns.abort(403, 'You cannot modify your own admin status')
            if 'email' in user_data or 'password' in user_data:
                users_ns.abort(400, 'You cannot modify your email or password')
                
        # Admin-specific email check
        if is_admin and 'email' in user_data:
            user_with_email = facade_instance.get_user_by_email(user_data['email'])
            if user_with_email and user_with_email.id != user_id:
                users_ns.abort(400, 'Email address is already registered')

        try:
            updated_user = facade_instance.update_user(user_id, data)
        except ValueError as e:
            users_ns.abort(400, str(e))

        if not updated_user:
            users_ns.abort(404, 'User not found')

        return updated_user.to_dict()

    @jwt_required()
    @users_ns.response(200, 'User successfully deleted')
    @users_ns.response(403, 'Admin privileges required')
    @users_ns.response(404, 'User not found')
    def delete(self, user_id):
        """Delete a user (Admin only)"""
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        if not is_admin: # <--- MODIFICATION: Admin check
            users_ns.abort(403, 'Admin privilege required to delete users')
        
        deleted = facade_instance.delete_user(user_id)
        if not deleted:
            users_ns.abort(404, 'User not found')
        return {"message": "User successfully deleted"}, 200
