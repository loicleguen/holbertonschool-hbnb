from flask import Flask
from flask_restx import Api
from app.api.v1.users import users_ns
from app.api.v1.amenities import amenities_ns

def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    # Placeholder for API namespaces (endpoints will be added later)
    # Additional namespaces for places, reviews, and amenities will be added later

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')

    return app

if __name__ == '__main__':
    # Ensure this runs the application correctly
    app = create_app()
    app.run(debug=True)
