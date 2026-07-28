#!/usr/bin/python3
"""Review endpoints — POST, GET, PUT, DELETE."""
from flask_restx import Namespace, Resource, fields
from app.services import hbnb_facade

api = Namespace("reviews", description="Review operations")

review_model = api.model("Review", {
    "text": fields.String(required=True, description="Text of the review"),
    "rating": fields.Integer(required=True, description="Rating of the place (1-5)"),
    "user_id": fields.String(required=True, description="ID of the user"),
    "place_id": fields.String(required=True, description="ID of the place")
})


@api.route("/")
class ReviewList(Resource):

    @api.expect(review_model, validate=True)
    @api.response(201, "Review successfully created")
    @api.response(400, "Invalid input data")
    def post(self):
        """Register a new review."""
        review_data = api.payload

        place = hbnb_facade.get_place(review_data.get("place_id"))
        if not place:
            return {"error": "Invalid input data"}, 400

        user = hbnb_facade.get_user(review_data.get("user_id"))
        if not user:
            return {"error": "Invalid input data"}, 400

        try:
            review = hbnb_facade.create_review(review_data)
        except ValueError as e:
            return {"error": str(e)}, 400

        return {
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "user_id": review.user.id,
            "place_id": review.place.id
        }, 201

    @api.response(200, "List of reviews retrieved successfully")
    def get(self):
        """Retrieve all reviews."""
        return [
            {
                "id": r.id,
                "text": r.text,
                "rating": r.rating
            }
            for r in hbnb_facade.get_all_reviews()
        ], 200


@api.route("/<review_id>")
class ReviewResource(Resource):

    @api.response(200, "Review details retrieved successfully")
    @api.response(404, "Review not found")
    def get(self, review_id):
        """Get review details by ID."""
        review = hbnb_facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return {
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "user_id": review.user.id,
            "place_id": review.place.id
        }, 200

    @api.expect(review_model, validate=True)
    @api.response(200, "Review updated successfully")
    @api.response(404, "Review not found")
    @api.response(400, "Invalid input data")
    def put(self, review_id):
        """Update a review's information."""
        if not hbnb_facade.get_review(review_id):
            return {"error": "Review not found"}, 404
        try:
            hbnb_facade.update_review(review_id, api.payload)
        except ValueError as e:
            return {"error": str(e)}, 400
        return {"message": "Review updated successfully"}, 200

    @api.response(200, "Review deleted successfully")
    @api.response(404, "Review not found")
    def delete(self, review_id):
        """Delete a review."""
        if not hbnb_facade.get_review(review_id):
            return {"error": "Review not found"}, 404
        hbnb_facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}, 200