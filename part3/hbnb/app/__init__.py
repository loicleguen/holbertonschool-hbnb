#!/usr/bin/python3
"""Initialize Flask app and register namespaces"""

from app.services.facade import HBnBFacade
from flask import Flask
from flask_restx import Api
from config import DevelopmentConfig
from flask_bcrypt import Bcrypt


facade = HBnBFacade()
bcrypt = Bcrypt()


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    bcrypt.init_app(app)

    # Initialisez l'API ici, en lui disant où servir la documentation (doc='/')
    # C'est la configuration par défaut, mais c'est bien de le savoir.
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='A simple API for HBnB by Loic',
        doc='/'  # URL pour la documentation Swagger
    )

    # Importez chaque namespace directement depuis son fichier
    from .api.v1.users import users_ns
    from .api.v1.places import places_ns
    from .api.v1.reviews import reviews_ns
    from .api.v1.amenities import amenities_ns

    # Ajoutez chaque namespace à l'API avec son préfixe de chemin
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')

    return app