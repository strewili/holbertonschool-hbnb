#!/usr/bin/python3
"""Module for Amenity class."""
from app.models.base_model import BaseModel
from app.extensions import db


class Amenity(BaseModel):
    """Represents an amenity associated with a Place."""
    __tablename__ = "amenities"

    name = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
