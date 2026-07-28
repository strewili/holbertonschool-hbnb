from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app.utils import admin_required
from app.services import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

@api.route('/')
class UserList(Resource):
    @admin_required
    @api.expect(user_model)
    def post(self):
        user_data = api.payload
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        new_user = facade.create_user(user_data)
        return {'id': new_user.id, 'message': 'User created'}, 201


@api.route('/<user_id>')
class UserResource(Resource):
    @jwt_required()
    def put(self, user_id):
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        if not is_admin and current_user_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        data = api.payload

        if not is_admin and ('email' in data or 'password' in data):
            return {'error': 'You cannot modify email or password'}, 400

        if is_admin and 'email' in data:
            existing_user = facade.get_user_by_email(data['email'])
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        updated_user = facade.update_user(user_id, data)
        return {'id': updated_user.id, 'message': 'User updated'}, 200
