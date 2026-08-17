from flask import Flask, send_from_directory
from flask_restx import Api

from app.config import config
from app.extensions import bcrypt, jwt, db

from app.api.v1.users import api as users_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns


def create_app(config_class=config['default']):
    app = Flask(
        __name__,
        static_folder='static',
        static_url_path=''
    )

    app.config.from_object(config_class)

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'
    )

    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(auth_ns, path="/api/v1/auth")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")

    @app.route('/')
    def home():
        return send_from_directory(
            app.static_folder,
            'index.html'
        )

    return app