#!/usr/bin/python3
"""Shared Flask extension instances (avoids circular imports)."""
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

bcrypt = Bcrypt()
jwt = JWTManager()
