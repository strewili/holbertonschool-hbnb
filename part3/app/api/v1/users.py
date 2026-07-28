#!/usr/bin/python3
"""User endpoints — POST, GET, PUT."""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade


api = Namespace("users", description="User operations")


user_model = api.model("User", {
    "first_name": fields.String(
        required=True,
        description="First name of the user"
    ),
    "last_name": fields.String(
        required=True,
        description="Last name of the user"
    ),
    "email": fields.String(
        required=True,
        description="Email address of the user"
    ),
    "password": fields.String(
        required=True,
        description="Password of the user"
    )
})


user_update_model = api.model("UserUpdate", {
    "first_name": fields.String(required=False),
    "last_name": fields.String(required=False),
    "email": fields.String(required=False),
    "password": fields.String(required=False)
})


@api.route("/")
class UserList(Resource):

    @api.expect(user_model, validate=True)
    @api.response(201, "User successfully created")
    @api.response(400, "Invalid input data")
    def post(self):
        """Register a new user."""

        user_data = api.payload

        if facade.get_user_by_email(user_data["email"]):
            return {
                "error": "Email already registered"
            }, 400

        try:
            user = facade.create_user(user_data)

        except ValueError as e:
            return {
                "error": str(e)
            }, 400

        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        }, 201


    @api.response(200, "List of users retrieved successfully")
    def get(self):
        """Retrieve all users."""

        users = facade.get_all_users()

        return [
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email
            }
            for user in users
        ], 200



@api.route("/<user_id>")
class UserResource(Resource):

    @api.response(200, "User details retrieved successfully")
    @api.response(404, "User not found")
    def get(self, user_id):
        """Get user details by ID."""

        user = facade.get_user(user_id)

        if not user:
            return {
                "error": "User not found"
            }, 404

        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        }, 200


    @jwt_required()
    @api.expect(user_update_model, validate=True)
    @api.response(200, "User updated successfully")
    @api.response(404, "User not found")
    @api.response(403, "Unauthorized action")
    @api.response(400, "Invalid input data")
    def put(self, user_id):
        """Update user information."""

        current_user_id = get_jwt_identity()
        claims = get_jwt()

        is_admin = claims.get("is_admin", False)

        if not is_admin and current_user_id != user_id:
            return {
                "error": "Unauthorized action"
            }, 403


        user = facade.get_user(user_id)

        if not user:
            return {
                "error": "User not found"
            }, 404


        data = api.payload


        if not is_admin and (
            "email" in data or "password" in data
        ):
            return {
                "error": "You cannot modify email or password"
            }, 400


        if is_admin and "email" in data:

            existing_user = facade.get_user_by_email(
                data["email"]
            )

            if existing_user and existing_user.id != user_id:
                return {
                    "error": "Email already in use"
                }, 400


        try:
            updated_user = facade.update_user(
                user_id,
                data
            )

        except ValueError as e:
            return {
                "error": str(e)
            }, 400


        return {
            "id": updated_user.id,
            "first_name": updated_user.first_name,
            "last_name": updated_user.last_name,
            "email": updated_user.email
        }, 200
