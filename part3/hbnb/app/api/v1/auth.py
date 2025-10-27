from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app import facade as facade_instance, bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request

auth_ns = Namespace('auth', description='Authentication operations')

# Model for login input
login_model = auth_ns.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

# Model for login response
login_response_model = auth_ns.model('LoginResponse', {
    'access_token': fields.String(description='JWT access token'),
    'user': fields.Nested(auth_ns.model('UserInfo', {
        'id': fields.String(description='User ID'),
        'email': fields.String(description='User email'),
        'first_name': fields.String(description='First name'),
        'last_name': fields.String(description='Last name'),
        'is_admin': fields.Boolean(description='Admin status')
    }))
})

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model, validate=True)
    @auth_ns.response(200, 'Login successful', login_response_model)
    @auth_ns.response(400, 'Invalid input')
    @auth_ns.response(401, 'Invalid credentials')
    def post(self):
        """Authenticate user and return JWT token"""
        credentials = request.get_json()
        email = credentials.get('email')
        password = credentials.get('password')
        
        if not email or not password:
            auth_ns.abort(400, 'Email and password are required')
        
        # Retrieve user by email
        user = facade_instance.get_user_by_email(email)
        
        if not user:
            auth_ns.abort(401, 'Invalid credentials')
        
        if not user.verify_password(password):
            auth_ns.abort(401, 'Invalid credentials')
        
        # Create JWT token with additional claims
        additional_claims = {
            'is_admin': user.is_admin,
            'email': user.email
        }
        access_token = create_access_token(
            identity=user.id,
            additional_claims=additional_claims
        )
        
        return {
            'access_token': access_token,
            'user': user.to_dict()  # Utilise to_dict() qui exclut le password
        }, 200

@auth_ns.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    @auth_ns.response(200, 'Access granted')
    @auth_ns.response(401, 'Unauthorized - Invalid or missing token')
    def get(self):
        """Example of a protected endpoint"""
        current_user_id = get_jwt_identity()
        user = facade_instance.get_user(current_user_id)
        
        if not user:
            auth_ns.abort(404, 'User not found')
        
        return {
            'message': f'Hello {user.first_name}!',
            'user_id': current_user_id
        }, 200