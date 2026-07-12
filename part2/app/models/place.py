#!/usr/bin/python3
"""Module for Place class."""
from app.models.base_model import BaseModel


class Place(BaseModel):
    """Represents a property listing."""

    def __init__(self, title, description, price,
                 latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("title is required and must be a string")
        if len(value) > 100:
            raise ValueError("title must not exceed 100 characters")
        self._title = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("price must be a positive number")
        self._price = float(value)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("latitude must be a number")
        if not (-90.0 <= value <= 90.0):
            raise ValueError("latitude must be between -90.0 and 90.0")
        self._latitude = float(value)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("longitude must be a number")
        if not (-180.0 <= value <= 180.0):
            raise ValueError("longitude must be between -180.0 and 180.0")
        self._longitude = float(value)

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value):
        from app.models.user import User
        if not isinstance(value, User):
            raise ValueError("owner must be a valid User instance")
        self._owner = value

    def add_review(self, review):
        """Add a review to this place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to this place."""
        self.amenities.append(amenity)
    
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
            {
                "id": amenity.id,
                "name": amenity.name
            }
            for amenity in self.amenities
        ]
    }
