<<<<<<< HEAD:part3/app/api/v1/amenities.py
﻿from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade
=======
from flask_restx import Namespace, Resource, fields
from app.services import hbnb_facade
>>>>>>> d75f672c609befe8f3c9a4fd6b4defa84bb1f822:part2/app/api/v1/amenities.py

api = Namespace("amenities", description="Amenity operations")

amenity_model = api.model("Amenity", {
    "name": fields.String(required=True,
                          description="Name of the amenity")
})


@api.route("/")
class AmenityList(Resource):

    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.response(201, "Amenity successfully created")
    @api.response(400, "Invalid input data")
    @api.response(403, "Admin privileges required")
    def post(self):
        """Register a new amenity (admin only)."""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {"error": "Admin privileges required"}, 403
        amenity_data = api.payload

        try:
            amenity = hbnb_facade.create_amenity(amenity_data)
        except ValueError as e:
            return {"error": str(e)}, 400

        return amenity.to_dict(), 201

    @api.response(200, "List of amenities retrieved successfully")
    def get(self):
        """Retrieve all amenities."""
        amenities = hbnb_facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200


@api.route("/<amenity_id>")
class AmenityResource(Resource):

    @api.response(200, "Amenity details retrieved successfully")
    @api.response(404, "Amenity not found")
    def get(self, amenity_id):
        """Retrieve an amenity by ID."""
        amenity = hbnb_facade.get_amenity(amenity_id)

        if not amenity:
            return {"error": "Amenity not found"}, 404

        return amenity.to_dict(), 200

    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.response(200, "Amenity updated successfully")
    @api.response(404, "Amenity not found")
    @api.response(400, "Invalid input data")
    def put(self, amenity_id):
        """Update an amenity (admin only)."""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {"error": "Admin privileges required"}, 403

        amenity = hbnb_facade.get_amenity(amenity_id)

        if not amenity:
            return {"error": "Amenity not found"}, 404

        try:
            hbnb_facade.update_amenity(amenity_id, api.payload)
        except ValueError as e:
            return {"error": str(e)}, 400

        updated = hbnb_facade.get_amenity(amenity_id)
        return updated.to_dict(), 200

