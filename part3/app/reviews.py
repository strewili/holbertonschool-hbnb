from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

@api.route('/<review_id>')
class ReviewResource(Resource):
    @jwt_required()
    def put(self, review_id):
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if not is_admin and review.user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        updated_review = facade.update_review(review_id, api.payload)
        return {'id': updated_review.id}, 200

    @jwt_required()
    def delete(self, review_id):
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if not is_admin and review.user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        facade.delete_review(review_id)
        return {'message': 'Review deleted'}, 200
