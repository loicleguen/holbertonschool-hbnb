#!/usr/bin/python3
"""Initialize Flask app and register namespaces"""

from app.services.facade import HBnBFacade
from flask import Flask
from flask_restx import Api
from app.api.v1.users import usersns
from app.api.v1.amenities import amenitiesns
from app.api.v1.places import placesns

facade = HBnBFacade()

def create_app():
    app = Flask(__name__)
    api = Api(app,
              version='1.0',
              title='HBnB API',
              description='HBnB Application API',
              doc='/api/v1/')
    
    usersns.facade = facade
    amenitiesns.facade = facade
    placesns.facade = facade

    # Register namespaces
    api.add_namespace(usersns, path='/api/v1/users')
    api.add_namespace(amenitiesns, path='/api/v1/amenities')
    api.add_namespace(placesns, path='/api/v1/places')

    return app
