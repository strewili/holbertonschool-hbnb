#!/usr/bin/python3
"""Module for Place class."""
from app.models.base_model import BaseModel
from app.extensions import db


place_amenity = db.Table(
    "place_amenity",
    db.Column("place_id", db.String(36),
              db.ForeignKey("places.id"), primary_key=True),
    db.Column("amenity_id", db.String(36),
              db.ForeignKey("amenities.id"), primary_key=True)
)


class Place(BaseModel):
    """Represents a property listing."""
    __tablename__ = "places"

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey("users.id"),
                          nullable=False)

    owner = db.relationship("User", backref="places")
    amenities = db.relationship(
        "Amenity",
        secondary=place_amenity,
        backref="places"
    )

    def __init__(self, title, description, price, latitude, longitude, owner):
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner": {
                "id": self.owner.id,
                "first_name": self.owner.first_name,
                "last_name": self.owner.last_name,
                "email": self.owner.email
            },
            "amenities": [
                {"id": a.id, "name": a.name}
                for a in self.amenities
            ]
        }
