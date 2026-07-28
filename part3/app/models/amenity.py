#!/usr/bin/python3
"""Module for Amenity class."""

from app.models.base_model import BaseModel
from app.extensions import db


place_amenity = db.Table(
    "place_amenity",
    db.Column(
        "place_id",
        db.String(36),
        db.ForeignKey("places.id"),
        primary_key=True
    ),
    db.Column(
        "amenity_id",
        db.String(36),
        db.ForeignKey("amenities.id"),
        primary_key=True
    )
)


class Amenity(BaseModel):
    """Represents an amenity associated with places."""

    __tablename__ = "amenities"

    name = db.Column(
        db.String(50),
        nullable=False
    )

    places = db.relationship(
        "Place",
        secondary=place_amenity,
        backref="amenities"
    )


    def __init__(self, name):
        self.name = name


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
