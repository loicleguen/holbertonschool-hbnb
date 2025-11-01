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
    'email': fields.String(required=False, description='Email of the user (admin only)'),
    'password': fields.String(required=False, description='Password of the user (admin only)'),
})


# ---------------------------
# User list and creation
# ---------------------------
@users_ns.route('/')
class UserList(Resource):

    @users_ns.expect(user_model, validate=True)
    @users_ns.response(201, 'User successfully created', user_response_model)
    @users_ns.response(400, 'Email already registered or invalid input')
    @users_ns.response(500, 'Internal server error')
    def post(self):
        """Register a new user"""
        user_data = request.get_json() or {}

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

    @users_ns.marshal_with(user_response_model)
    @users_ns.response(200, 'User details retrieved successfully')
    @users_ns.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade_instance.get_user(user_id) 
        if not user:
            users_ns.abort(404, 'User not found')
        return user.to_dict()

    @jwt_required()
    @users_ns.expect(user_update_model, validate=True)
    @users_ns.marshal_with(user_response_model) 
    @users_ns.response(200, 'User successfully updated')
    @users_ns.response(400, 'Invalid input data')
    @users_ns.response(403, 'Unauthorized action')
    @users_ns.response(404, 'User not found')
    def put(self, user_id):
        """Update user profile (users can update first_name/last_name, admins can update everything)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        # Check if user can modify this profile
        if current_user_id != user_id and not is_admin:
            users_ns.abort(403, 'Unauthorized action')
        
        data = users_ns.payload

        # For non-admin users, block email and password changes
        if not is_admin:
            if 'email' in data or 'password' in data:
                users_ns.abort(403, 'You cannot change your email address or your password !')

        # For admin users, check email uniqueness if email is being changed
        if is_admin and 'email' in data:
            existing_user = facade_instance.get_user_by_email(data['email'])
            if existing_user and existing_user.id != user_id:
                users_ns.abort(400, 'Email already in use')

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
        """Delete a user by ID (admin only)"""
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        # Only admins can delete users
        if not is_admin:
            users_ns.abort(403, 'Admin privileges required')
        
        deleted = facade_instance.delete_user(user_id)
        if not deleted:
            users_ns.abort(404, 'User not found')
        return {"message": "User successfully deleted"}, 200