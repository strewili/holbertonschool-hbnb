#!/usr/bin/python3
"""Module for Amenity class."""
from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """Represents an amenity associated with a Place."""

    def __init__(self, name):
        super().__init__()
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("name is required and must be a string")
        if len(value) > 50:
            raise ValueError("name must not exceed 50 characters")
        self._name = value