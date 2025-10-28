#!/usr/bin/python3
"""Initialize Flask app and register namespaces"""

from app.services.facade import HBnBFacade
from flask import Flask
from flask_restx import Api
from config import DevelopmentConfig
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

jwt = JWTManager()
facade = HBnBFacade()
bcrypt = Bcrypt()


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Initialize the API here, specifying where to serve the documentation (doc='/')
    # This is the default configuration, but it's good to be aware of it.
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='A simple API for HBnB by Loic & Val',
        doc='/'  # URL for Swagger documentation
    )

    # Import each namespace directly from its file
    from .api.v1.users import users_ns
    from .api.v1.places import places_ns
    from .api.v1.reviews import reviews_ns
    from .api.v1.amenities import amenities_ns
    from .api.v1.auth import auth_ns

    # Add each namespace to the API with its path prefix
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    return app