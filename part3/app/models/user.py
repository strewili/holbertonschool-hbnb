#!/usr/bin/python3
"""Module for User model."""

from app.models.base_model import BaseModel
from app.extensions import db, bcrypt


class User(BaseModel):
    """Represents a registered user."""

    __tablename__ = "users"

    first_name = db.Column(
        db.String(50),
        nullable=False
    )

    last_name = db.Column(
        db.String(50),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(128),
        nullable=False
    )

    is_admin = db.Column(
        db.Boolean,
        default=False
    )


    def __init__(
        self,
        first_name,
        last_name,
        email,
        password,
        is_admin=False
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin


    @property
    def password(self):
        return self._password


    @password.setter
    def password(self, value):
        if not value or not isinstance(value, str):
            raise ValueError(
                "password is required and must be a string"
            )

        self._password = bcrypt.generate_password_hash(
            value
        ).decode("utf-8")


    def verify_password(self, password):
        return bcrypt.check_password_hash(
        self.password,
        password
    )

