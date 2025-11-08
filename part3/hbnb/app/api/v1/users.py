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

# Model for USER update (PUT) - first_name et last_name uniquement
user_update_model = users_ns.model('UserUpdateInput', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Current email (for verification)'),
    'password': fields.String(required=True, description='Current password (for verification)'),
})

# Model for ADMIN update (PUT) - Tous les champs modifiables
admin_update_model = users_ns.model('AdminUpdateInput', {
    'first_name': fields.String(required=False, description='First name of the user'),
    'last_name': fields.String(required=False, description='Last name of the user'),
    'email': fields.String(required=False, description='New email address'),
    'password': fields.String(required=False, description='New password'),
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
# User self-update (own profile only)
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
    @users_ns.response(401, 'Invalid email or password')
    @users_ns.response(403, 'Unauthorized - Admins must use /api/v1/users/admin/{user_id}')
    @users_ns.response(404, 'User not found')
    def put(self, user_id):
        """Update own profile (requires email and password verification) - Users can only update first_name and last_name"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        # Only the user themselves can use this endpoint
        if current_user_id != user_id:
            if is_admin:
                users_ns.abort(403, 'Admins must use /api/v1/users/admin/{user_id} endpoint')
            else:
                users_ns.abort(403, 'Unauthorized action')
        
        data = users_ns.payload
        
        # Get the user to verify credentials
        user = facade_instance.get_user(user_id)
        if not user:
            users_ns.abort(404, 'User not found')
        
        # Verify email and password
        if user.email != data.get('email') or not user.verify_password(data.get('password', '')):
            users_ns.abort(401, 'Invalid email or password')
        
        # Prepare update data (only first_name and last_name)
        update_data = {
            'first_name': data['first_name'],
            'last_name': data['last_name']
        }

        try:
            updated_user = facade_instance.update_user(user_id, update_data)
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


# ---------------------------
# Admin-only user update (can modify ALL fields)
# ---------------------------
@users_ns.route('/admin/<string:user_id>')
class AdminUserResource(Resource):

    @jwt_required()
    @users_ns.expect(admin_update_model, validate=True)
    @users_ns.marshal_with(user_response_model) 
    @users_ns.response(200, 'User successfully updated by admin')
    @users_ns.response(400, 'Invalid input data or email already in use')
    @users_ns.response(403, 'Admin privileges required')
    @users_ns.response(404, 'User not found')
    def put(self, user_id):
        """Update any user profile (admin only) - Can modify all fields including email and password"""
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        # Only admins can use this endpoint
        if not is_admin:
            users_ns.abort(403, 'Admin privileges required')
        
        data = users_ns.payload
        
        # Get the user
        user = facade_instance.get_user(user_id)
        if not user:
            users_ns.abort(404, 'User not found')
        
        # Check email uniqueness if email is being changed
        if 'email' in data and data['email']:
            existing_user = facade_instance.get_user_by_email(data['email'])
            if existing_user and existing_user.id != user_id:
                users_ns.abort(400, 'Email already in use')

        # Remove empty fields
        update_data = {k: v for k, v in data.items() if v not in [None, '', []]}

        try:
            updated_user = facade_instance.update_user(user_id, update_data)
        except ValueError as e:
            users_ns.abort(400, str(e))

        if not updated_user:
            users_ns.abort(404, 'User not found')

        return updated_user.to_dict()