﻿from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ── Users ──────────────────────────────────────────────────
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute("email", email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        return self.user_repo.update(user_id, data)

    # ── Amenities ──────────────────────────────────────────────
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        return self.amenity_repo.update(amenity_id, data)

    # ── Places ─────────────────────────────────────────────────
    def create_place(self, place_data):
        owner = self.get_user(place_data.get("owner_id"))
        if not owner:
            return None
        place = Place(
            title=place_data["title"],
            description=place_data.get("description", ""),
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner=owner
        )
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        return self.place_repo.update(place_id, data)

    # ── Reviews ────────────────────────────────────────────────
    def create_review(self, review_data):
        place = self.get_place(review_data.get("place_id"))
        user = self.get_user(review_data.get("user_id"))
        if not place or not user:
            return None
        review = Review(
            text=review_data["text"],
            rating=review_data["rating"],
            place=place,
            user=user
        )
        self.review_repo.add(review)
        place.add_review(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

        def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)
        return place.reviews if place else None

    def update_review(self, review_id, data):
        review = self.get_review(review_id)

        if not review:
            return None

        if "text" in data:
            review.text = data["text"]

        if "rating" in data:
            review.rating = data["rating"]

        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)

        if not review:
            return False

        if review in review.place.reviews:
            review.place.reviews.remove(review)

        self.review_repo.delete(review_id)
        return True
