#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import HBnBFacade



# Namespace
usersns = Namespace('users', description='User operations')

# User model pour validation et documentation
user_model = usersns.model('User', {

    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

# Modèle pour la mise à jour d'un utilisateur (PUT)
user_update_model = usersns.model('UserUpdate', {
    'first_name': fields.String(required=False, description='First name of the user'),
    'last_name': fields.String(required=False, description='Last name of the user')
})



# ---------------------------
# Liste des utilisateurs et création
# ---------------------------
@usersns.route('/')
class UserList(Resource):

    @usersns.expect(user_model, validate=True)
    @usersns.response(201, 'User successfully created')
    @usersns.response(400, 'Email already registered or invalid input')
    def post(self):
        """Register a new user"""
        user_data = request.get_json() or {}


        try:
            new_user = usersns.facade.create_user(user_data)
        except (ValueError, TypeError) as e:
            return {'error': str(e)}, 400
        except Exception:
            return {'error': 'Internal server error'}, 500

        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201

    @usersns.response(200, 'List of users retrieved successfully')
    def get(self):
        """List all users"""
        users = usersns.facade.get_all_user()
        return [
            {
                'id': u.id,
                'first_name': u.first_name,
                'last_name': u.last_name,
                'email': u.email
            } for u in users
        ], 200


# ---------------------------
# Détails et mise à jour d'un utilisateur
# ---------------------------
@usersns.route('/<string:user_id>')
class UserResource(Resource):

    @usersns.response(200, 'User details retrieved successfully')
    @usersns.response(404, 'User not found')

    def get(self, user_id):
        """Get user details by ID"""
        user = usersns.facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @usersns.expect(user_update_model, validate=True)
    @usersns.response(200, 'User successfully updated')
    @usersns.response(400, 'Invalid input data')
    @usersns.response(404, 'User not found')

    def put(self, user_id):
        """Update an existing user by ID"""
        data = request.get_json() or {}

        try:
            updated_user = usersns.facade.update_user(user_id, data)
        except ValueError as e:
            return {'error': str(e)}, 400

        if not updated_user:
            return {'error': 'User not found'}, 404

        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200
