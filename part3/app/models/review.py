#!/usr/bin/python3
"""Module for Review class."""

from app.models.base_model import BaseModel
from app.extensions import db


class Review(BaseModel):
    """Represents a review written by a user for a place."""

    __tablename__ = "reviews"

    text = db.Column(
        db.Text,
        nullable=False
    )

    rating = db.Column(
        db.Integer,
        nullable=False
    )

    place_id = db.Column(
        db.String(36),
        db.ForeignKey("places.id"),
        nullable=False
    )

    user_id = db.Column(
        db.String(36),
        db.ForeignKey("users.id"),
        nullable=False
    )

    user = db.relationship(
        "User",
        backref="reviews"
    )


    def __init__(self, text, rating, place, user):
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user


    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place_id,
            "user_id": self.user_id
        }
