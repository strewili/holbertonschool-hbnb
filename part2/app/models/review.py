#!/usr/bin/python3
"""Module for Review class."""
from app.models.base_model import BaseModel


class Review(BaseModel):
    """Represents a review written by a user for a place."""

    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("text is required and must be a string")
        self._text = value

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int) or not (1 <= value <= 5):
            raise ValueError("rating must be an integer between 1 and 5")
        self._rating = value

    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, value):
        from app.models.place import Place
        if not isinstance(value, Place):
            raise ValueError("place must be a valid Place instance")
        self._place = value

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        from app.models.user import User
        if not isinstance(value, User):
            raise ValueError("user must be a valid User instance")
        self._user = value