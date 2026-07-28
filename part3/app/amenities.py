from flask_restx import Namespace, Resource, fields
from app.utils import admin_required
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True)
})

@api.route('/')
class AmenityList(Resource):
    @admin_required
    @api.expect(amenity_model)
    def post(self):
        new_amenity = facade.create_amenity(api.payload)
        return {'id': new_amenity.id}, 201


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @admin_required
    @api.expect(amenity_model)
    def put(self, amenity_id):
        updated = facade.update_amenity(amenity_id, api.payload)
        return {'id': updated.id, 'message': 'Amenity updated'}, 200
