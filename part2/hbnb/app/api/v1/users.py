from flask_restx import Namespace, Resource, fields
from flask import request
from app import facade as facade_instance



# Namespace
usersns = Namespace('users', description='User operations')

<<<<<<< HEAD
# User model for validation and documentation (Input)
user_model = usersns.model('UserInput', {
=======
# User model pour validation et documentation
user_model = usersns.model('User', {

>>>>>>> d93215b66c691f44bbaebe3e4250ba9e64830dd7
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    # 'password' removed
})

# User model for API Response
user_response_model = usersns.model('UserResponse', {
    'id': fields.String(description='User unique identifier'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user')
})

# Model for user update (PUT)
user_update_model = usersns.model('UserUpdateInput', {
    'first_name': fields.String(required=False, description='First name of the user'),
    'last_name': fields.String(required=False, description='Last name of the user')
})



# ---------------------------
# User list and creation
# ---------------------------
@usersns.route('/')
class UserList(Resource):

    @usersns.expect(user_model, validate=True)
    @usersns.response(201, 'User successfully created', user_response_model)
    @usersns.response(400, 'Email already registered or invalid input')
    @usersns.response(500, 'Internal server error')
    def post(self):
        """Register a new user"""
        user_data = request.get_json() or {}


        try:
            # Uses the global user_facade instance
            new_user = facade_instance.create_user(user_data)
        except (ValueError, TypeError) as e:
            # 400 Bad Request for validation errors
            usersns.abort(400, message=str(e))
        except Exception:
            # 500 Internal Server Error for unhandled exceptions
            usersns.abort(500, message='Internal server error')

        # to_dict() should be defined on the BaseModel
        return new_user.to_dict(), 201

    @usersns.marshal_list_with(user_response_model)
    @usersns.response(200, 'List of users retrieved successfully')
    def get(self):
        """List all users"""
        # Uses the global user_facade instance
        users = facade_instance.get_all_user()
        
        return [u.to_dict() for u in users]


# ---------------------------
# User details and update/delete
# ---------------------------
@usersns.route('/<string:user_id>')
class UserResource(Resource):

    @usersns.marshal_with(user_response_model)
    @usersns.response(200, 'User details retrieved successfully')
    @usersns.response(404, 'User not found')

    def get(self, user_id):
        """Get user details by ID"""
        # Uses the global user_facade instance
        user = facade_instance.get_user(user_id) 
        if not user:
            usersns.abort(404, 'User not found')
        return user.to_dict()

    @usersns.expect(user_update_model, validate=True)
    @usersns.marshal_with(user_response_model) 
    @usersns.response(200, 'User successfully updated')
    @usersns.response(400, 'Invalid input data')
    @usersns.response(404, 'User not found')

    def put(self, user_id):
        """Update an existing user by ID"""
        data = request.get_json() or {}

        try:
            # Uses the global user_facade instance
            updated_user = facade_instance.update_user(user_id, data)
        except ValueError as e:
            # 400 Bad Request for validation errors from update_user
            usersns.abort(400, message=str(e))

        if not updated_user:
            usersns.abort(404, 'User not found')

        return updated_user.to_dict()

    @usersns.response(204, 'User successfully deleted')
    @usersns.response(404, 'User not found')
    def delete(self, user_id):
        """Delete a user by ID"""
        deleted = facade_instance.delete_user(user_id)
        if not deleted:
            usersns.abort(404, 'User not found')
        return {"message": "User is deleted"}, 200