#!/usr/bin/python3
"""Application configuration classes.

Lives at the project root so it can be loaded as ``config.<ClassName>``,
e.g. ``create_app("config.DevelopmentConfig")``.
"""

import os


class Config:
    """Base configuration shared by every environment."""

    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-super-secret-key')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """Local development: SQLite database and debug mode on."""

    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///development.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    """Automated tests: separate database, debug off."""

    TESTING = True
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.getenv(
        'TEST_DATABASE_URL',
        'sqlite:///test.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """Production: MySQL, debug off."""

    DEBUG = False

    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://hbnb_user:hbnb_pwd@localhost/hbnb_prod'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
