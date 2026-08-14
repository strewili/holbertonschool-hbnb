#!/usr/bin/python3
"""Application factory for the HBnB API."""

from flask import Flask
from flask_cors import CORS
from flask_restx import Api

from app.extensions import bcrypt, jwt, db

from app.api.v1.users import api as users_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns


def create_app(config_class="config.DevelopmentConfig"):
    """Build and configure a Flask application instance.

    Args:
        config_class: dotted path (or class object) of the configuration
            to load, e.g. ``"config.ProductionConfig"``.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    # Allow the Part 4 web client to call this API from the browser.
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Tables are auto-created for development/testing only.
    # In production the schema is created by the SQL scripts.
    if app.config.get("DEBUG") or app.config.get("TESTING"):
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

    return app
