#!/usr/bin/python3
"""Module for Place class."""

from app.models.base_model import BaseModel
from app.extensions import db


class Place(BaseModel):
    """Represents a property listing."""

    __tablename__ = "places"

    title = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    latitude = db.Column(
        db.Float,
        nullable=False
    )

    longitude = db.Column(
        db.Float,
        nullable=False
    )

    owner_id = db.Column(
        db.String(36),
        db.ForeignKey("users.id"),
        nullable=False
    )

    owner = db.relationship(
        "User",
        backref="places"
    )

    reviews = db.relationship(
        "Review",
        backref="place",
        cascade="all, delete-orphan"
    )


    def __init__(
        self,
        title,
        description,
        price,
        latitude,
        longitude,
        owner
    ):
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner


    def add_review(self, review):
        """Add review."""
        self.reviews.append(review)


    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id
        }
