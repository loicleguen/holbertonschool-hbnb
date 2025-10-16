from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

facade = HBnBFacade()

reviews_ns = Namespace('reviews', description='Review operations')

review_model = reviews_ns.model('ReviewInput', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

review_response_model = reviews_ns.model('ReviewResponse', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user'),
    'place_id': fields.String(description='ID of the place'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp'),
})

review_update_model = reviews_ns.model('ReviewUpdate', {
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)')
})


@reviews_ns.route('/')
class ReviewList(Resource):
    @reviews_ns.expect(review_model, validate=True)
    @reviews_ns.response(201, 'Review successfully created', review_response_model)
    @reviews_ns.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        try:
            review = facade.create_review(reviews_ns.payload)
            return review.to_dict(), 201
        except ValueError as e:
            reviews_ns.abort(400, str(e))
        except Exception as e:
            reviews_ns.abort(500, f"Internal error: {str(e)}")

    @reviews_ns.marshal_list_with(review_response_model)
    @reviews_ns.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [r.to_dict() for r in reviews], 200

@reviews_ns.route('/<string:review_id>')
@reviews_ns.param('review_id', 'The Review identifier (UUID)')
class ReviewResource(Resource):
    @reviews_ns.marshal_with(review_response_model)
    @reviews_ns.response(200, 'Review details retrieved successfully')
    @reviews_ns.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            reviews_ns.abort(404, 'Review not found')
        return review.to_dict(), 200

    @reviews_ns.expect(review_update_model, validate=True)
    @reviews_ns.response(200, 'Review updated successfully')
    @reviews_ns.response(404, 'Review not found')
    @reviews_ns.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        try:
            updated_review = facade.update_review(review_id, reviews_ns.payload)
            if not updated_review:
                reviews_ns.abort(404, 'Review not found')
            return {"message": "Review updated successfully"}, 200
        except ValueError as e:
            reviews_ns.abort(400, str(e))
        except Exception as e:
            reviews_ns.abort(500, f"Internal error: {str(e)}")

    @reviews_ns.response(200, 'Review deleted successfully')
    @reviews_ns.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        if facade.delete_review(review_id):
            return {"message": "Review deleted successfully"}, 200
        reviews_ns.abort(404, 'Review not found')


@reviews_ns.route('/places/<string:place_id>/reviews')
@reviews_ns.param('place_id', 'The Place identifier (UUID)')
class PlaceReviewList(Resource):
    @reviews_ns.marshal_list_with(review_response_model)
    @reviews_ns.response(200, 'List of reviews for the place retrieved successfully')
    @reviews_ns.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)

        if reviews is None:
            reviews_ns.abort(404, 'Place not found')

        return [r.to_dict() for r in reviews], 200
