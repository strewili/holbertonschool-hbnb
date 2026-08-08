#!/usr/bin/python3
"""Module for Review class."""
from sqlalchemy.orm import validates

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
    place = db.relationship(
        "Place",
        backref="reviews"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "user_id", "place_id",
            name="uq_review_user_place"
        ),
    )

    def __init__(self, text, rating, place, user):
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    @validates("rating")
    def validate_rating(self, key, value):
        """Ensure the rating is an integer between 1 and 5."""
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError("Rating must be an integer between 1 and 5")

        if value < 1 or value > 5:
            raise ValueError("Rating must be an integer between 1 and 5")

        return value

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place_id,
            "user_id": self.user_id
        }
