#!/usr/bin/python3
"""Initialize Flask app and register namespaces"""

from app.services.facade import HBnBFacade
from flask import Flask
from flask_restx import Api

from app.api.v1.users import users_ns
from app.api.v1.amenities import amenities_ns
from app.api.v1.places import places_ns
from app.api.v1.reviews import reviews_ns

facade = HBnBFacade()


def create_app():
    app = Flask(__name__)
    api = Api(app,
              version='1.0',
              title='HBnB API',
              description='HBnB Application API',
              doc='/api/v1/')
    
    users_ns.facade = facade
    amenities_ns.facade = facade
    places_ns.facade = facade
    reviews_ns.facade = facade


    # Register namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')


    return app
