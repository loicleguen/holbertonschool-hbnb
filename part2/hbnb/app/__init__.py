#!/usr/bin/python3
"""Initialize Flask app and register namespaces"""

from flask import Flask
from flask_restx import Api
from app.api.v1.users import usersns


def create_app():
    app = Flask(__name__)
    api = Api(app,
              version='1.0',
              title='HBnB API',
              description='HBnB Application API',
              doc='/api/v1/')

    # Register namespaces
    api.add_namespace(usersns, path='/api/v1/users')

    return app
