#!/usr/bin/python3
"""Review endpoints."""
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace("reviews", description="Review operations")

review_model = api.model("Review", {
    "text": fields.String(required=True, description="Review text"),
    "rating": fields.Integer(required=True, description="Rating from 1 to 5"),
    "user_id": fields.String(required=True, description="User ID"),
    "place_id": fields.String(required=True, description="Place ID")
})

review_update_model = api.model("ReviewUpdate", {
    "text": fields.String(required=False, description="Review text"),
    "rating": fields.Integer(
        required=False,
        description="Rating from 1 to 5"
    )
})


def serialize_review(review):
    """Convert a Review object to dictionary."""
    return {
        "id": review.id,
        "text": review.text,
        "rating": review.rating,
        "user_id": review.user.id,
        "place_id": review.place.id
    }


@api.route("/")
class ReviewList(Resource):
    """Review list operations."""

    @api.expect(review_model, validate=True)
    def post(self):
        """Create a new review."""
        try:
            review = facade.create_review(api.payload)
        except ValueError as e:
            return {"error": str(e)}, 400

        if not review:
            return {"error": "User or Place not found"}, 404

        return serialize_review(review), 201

    def get(self):
        """Retrieve all reviews."""
        reviews = facade.get_all_reviews()
        return [serialize_review(review) for review in reviews], 200


@api.route("/<review_id>")
class ReviewResource(Resource):
    """Single review operations."""

    def get(self, review_id):
        """Retrieve a review by ID."""
        review = facade.get_review(review_id)

        if not review:
            return {"error": "Review not found"}, 404

        return serialize_review(review), 200

    @api.expect(review_update_model, validate=True)
    def put(self, review_id):
        """Update a review."""
        review = facade.get_review(review_id)

        if not review:
            return {"error": "Review not found"}, 404

        try:
            updated_review = facade.update_review(review_id, api.payload)
        except ValueError as e:
            return {"error": str(e)}, 400

        return serialize_review(updated_review), 200

    def delete(self, review_id):
        """Delete a review."""
        review = facade.get_review(review_id)

        if not review:
            return {"error": "Review not found"}, 404

        facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}, 200
