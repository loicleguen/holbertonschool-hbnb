from flask_restx import Namespace, Resource, fields
from flask import request
from app import facade as facade_instance
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

reviews_ns = Namespace('reviews', description='Review operations')


# -----------------------
# Models for Swagger
# -----------------------
review_place_nested_model = reviews_ns.model('ReviewPlaceNested', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title of the place'),
})

review_user_nested_model = reviews_ns.model('ReviewUserNested', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
})

review_model = reviews_ns.model('ReviewInput', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Float(required=True, description='Rating of the place (1.0-5.0)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

review_response_model = reviews_ns.model('ReviewResponse', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Float(description='Rating of the place (1.0-5.0)'),
    'user': fields.Nested(review_user_nested_model, description='User who wrote the review'),
    'place': fields.Nested(review_place_nested_model, description='Place being reviewed'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp'),
})

review_update_model = reviews_ns.model('ReviewUpdate', {
    'text': fields.String(description='Text of the review'),
    'rating': fields.Float(description='Rating of the place (1.0-5.0)')
})


# -----------------------
# Routes
# -----------------------
@reviews_ns.route('/')
class ReviewList(Resource):
    
    @jwt_required()
    @reviews_ns.expect(review_model, validate=True)
    @reviews_ns.response(201, 'Review successfully created', review_response_model)
    @reviews_ns.response(400, 'Invalid input data')
    @reviews_ns.response(403, 'Unauthorized action')
    @reviews_ns.response(409, 'User has already reviewed this place')
    def post(self):
        """Register a new review (Protected - authentication required)"""
        current_user_id = get_jwt_identity()
        
        try:
            review_data = reviews_ns.payload
            
            # Verify that the user_id matches the authenticated user
            if review_data.get('user_id') != current_user_id:
                reviews_ns.abort(403, 'You can only create reviews for yourself')
            
            place_id = review_data.get('place_id')
            
            # Check if the place exists and get the owner
            place = facade_instance.get_place(place_id)
            if not place:
                reviews_ns.abort(404, 'Place not found')
            
            # Check if user is trying to review their own place
            if place.owner_id == current_user_id:
                reviews_ns.abort(403, 'You cannot review your own place')
            
            # Check if user has already reviewed this place
            if facade_instance.user_has_reviewed_place(current_user_id, place_id):
                reviews_ns.abort(409, 'You have already reviewed this place')
            
            review = facade_instance.create_review(review_data)
            
            # SQLAlchemy charge automatiquement user et place
            return review.to_dict(), 201
            
        except ValueError as e:
            reviews_ns.abort(400, str(e))
        except Exception as e:
            reviews_ns.abort(500, f"Internal error: {str(e)}")

    @reviews_ns.marshal_list_with(review_response_model)
    @reviews_ns.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews (Public)"""
        reviews = facade_instance.get_all_reviews()
        
        # SQLAlchemy charge automatiquement user et place pour chaque review
        return [r.to_dict() for r in reviews]


@reviews_ns.route('/<string:review_id>')
@reviews_ns.param('review_id', 'The Review identifier (UUID)')
class ReviewResource(Resource):
    
    @reviews_ns.marshal_with(review_response_model)
    @reviews_ns.response(200, 'Review details retrieved successfully')
    @reviews_ns.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID (Public)"""
        review = facade_instance.get_review(review_id)
        if not review:
            reviews_ns.abort(404, 'Review not found')
        
        # SQLAlchemy charge automatiquement user et place
        return review.to_dict()

    @jwt_required()
    @reviews_ns.expect(review_update_model, validate=True)
    @reviews_ns.response(200, 'Review updated successfully', review_response_model)
    @reviews_ns.response(404, 'Review not found')
    @reviews_ns.response(400, 'Invalid input data')
    @reviews_ns.response(403, 'Unauthorized action')
    def put(self, review_id):
        """Update a review's information (Protected - author or admin)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        # Get the review to check authorship
        review = facade_instance.get_review(review_id)
        if not review:
            reviews_ns.abort(404, 'Review not found')
        
        # Check if user is the author or admin
        if review.user_id != current_user_id and not is_admin:
            reviews_ns.abort(403, 'You can only update your own reviews')
        
        try:
            updated_review = facade_instance.update_review(review_id, reviews_ns.payload)
            if not updated_review:
                reviews_ns.abort(404, 'Review not found')

            # SQLAlchemy charge automatiquement user et place
            return updated_review.to_dict()

        except ValueError as e:
            reviews_ns.abort(400, str(e))
        except Exception as e:
            reviews_ns.abort(500, f"Internal error: {str(e)}")

    @jwt_required()
    @reviews_ns.response(204, 'Review deleted successfully')
    @reviews_ns.response(404, 'Review not found')
    @reviews_ns.response(403, 'Unauthorized action')
    def delete(self, review_id):
        """Delete a review (Protected - author or admin only)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        # Get the review to check authorship
        review = facade_instance.get_review(review_id)
        if not review:
            reviews_ns.abort(404, 'Review not found')
        
        # Check if user is the author or admin
        if review.user_id != current_user_id and not is_admin:
            reviews_ns.abort(403, 'You can only delete your own reviews')
        
        if facade_instance.delete_review(review_id):
            return {}, 204
        reviews_ns.abort(404, 'Review not found')


@reviews_ns.route('/places/<string:place_id>/reviews')
@reviews_ns.param('place_id', 'The Place identifier (UUID)')
class PlaceReviewList(Resource):

    @reviews_ns.marshal_list_with(review_response_model)
    @reviews_ns.response(200, 'List of reviews for the place retrieved successfully')
    @reviews_ns.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place (Public)"""
        reviews_data = facade_instance.get_reviews_by_place(place_id)

        if reviews_data is None:
            reviews_ns.abort(404, 'Place not found')

        reviews = reviews_data if isinstance(reviews_data, list) else [reviews_data]

        # SQLAlchemy charge automatiquement user et place pour chaque review
        return [r.to_dict() for r in reviews]