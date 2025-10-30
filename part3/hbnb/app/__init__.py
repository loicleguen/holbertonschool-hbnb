#!/usr/bin/python3
"""Initialize Flask app and register namespaces"""

from app.services.facade import HBnBFacade
from flask import Flask
from flask_restx import Api
from config import DevelopmentConfig
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

jwt = JWTManager()
facade = HBnBFacade()
bcrypt = Bcrypt()
db = SQLAlchemy()


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)


    # Configure JWT authorization in Swagger
    authorizations = {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
        }
    }

    # Initialize the API with JWT authorization support
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='A simple API for HBnB by Loic & Val',
        doc='/',
        authorizations=authorizations,  # Add JWT configuration
        security='Bearer'  # Apply globally (can be overridden per endpoint)
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