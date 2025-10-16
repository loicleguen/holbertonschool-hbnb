#!/usr/bin/python3
"""Initialize Flask app and register namespaces"""

from app.services.facade import HBnBFacade
from flask import Flask
from flask_restx import Api

<<<<<<< HEAD
=======
from app.api.v1.users import usersns
from app.api.v1.amenities import amenitiesns
from app.api.v1.places import placesns
>>>>>>> d93215b66c691f44bbaebe3e4250ba9e64830dd7

facade = HBnBFacade()


def create_app():
    app = Flask(__name__)
    api = Api(app,
              version='1.0',
              title='HBnB API',
              description='HBnB Application API',
              doc='/api/v1/')
    
    from app.api.v1.users import usersns
    from app.api.v1.amenities import amenitiesns
    from app.api.v1.places import placesns
    from app.api.v1.reviews import reviewsns


    # Register namespaces
    api.add_namespace(usersns, path='/api/v1/users')
    api.add_namespace(amenitiesns, path='/api/v1/amenities')
    api.add_namespace(placesns, path='/api/v1/places')
    api.add_namespace(reviewsns, path='/api/v1/reviews')


    return app
