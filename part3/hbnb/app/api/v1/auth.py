from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import facade as facade_instance


auth_ns = Namespace('auth', description='Authentication operations')

# Model for login input
login_model = auth_ns.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

# Model for login response
login_response_model = auth_ns.model('LoginResponse', {
    'access_token': fields.String(description='JWT access token')
})

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model, validate=True)
    @auth_ns.response(200, 'Login successful', login_response_model)
    @auth_ns.response(400, 'Invalid input')
    @auth_ns.response(401, 'Invalid credentials')
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = auth_ns.payload
        
        # Step 1: Retrieve the user based on the provided email
        user = facade_instance.get_user_by_email(credentials['email'])
        
        # Step 2: Check if the user exists and the password is correct
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Step 3: Create a JWT token with the user's id and is_admin flag
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"is_admin": user.is_admin}
        )
        
        # Step 4: Return the JWT token to the client
        return {'access_token': access_token}, 200


@auth_ns.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    @auth_ns.response(200, 'Access granted')
    @auth_ns.response(401, 'Unauthorized - Invalid or missing token')
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        current_user = get_jwt_identity()
        return {'message': f'Hello, user {current_user}'}, 200