#!/usr/bin/python3
"""Place review endpoints."""

from flask_restx import Namespace, Resource
from app.services import facade


api = Namespace("places", description="Place operations")


@api.route("/<place_id>/reviews")
class PlaceReviewList(Resource):
    """Reviews associated with a specific place."""

    @api.response(200, "Reviews retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Retrieve all reviews for a specific place."""
        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        reviews = facade.get_reviews_by_place(place_id)

        return [
            {
                "id": review.id,
                "text": review.text,
                "rating": review.rating,
                "user_id": review.user.id,
                "place_id": review.place.id
            }
            for review in reviews
        ], 200
