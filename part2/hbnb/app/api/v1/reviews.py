from flask_restx import Namespace, Resource, fields
from flask import request
from app import facade as facade_instance

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
    'rating': fields.Float(required=True, description='Rating of the place (1.0-5.0)'), # Expects float
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
    
    @reviews_ns.expect(review_model, validate=True)
    @reviews_ns.response(201, 'Review successfully created', review_response_model)
    @reviews_ns.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        try:
            review = facade_instance.create_review(reviews_ns.payload)
            
            user_obj = facade_instance.get_user(review.user_id)
            place_obj = facade_instance.get_place(review.place_id)
            
            return review.to_dict(
                users_map={review.user_id: user_obj},
                places_map={review.place_id: place_obj}
            ), 201
            
        except ValueError as e:
            reviews_ns.abort(400, str(e))
        except Exception as e:
            reviews_ns.abort(500, f"Internal error: {str(e)}")

    @reviews_ns.marshal_list_with(review_response_model)
    @reviews_ns.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade_instance.get_all_reviews()
        
        user_ids = {r.user_id for r in reviews if r.user_id}
        place_ids = {r.place_id for r in reviews if r.place_id}

        users = {u.id: u for u in facade_instance.get_users_by_ids(list(user_ids))}
        places = {p.id: p for p in facade_instance.get_places_by_ids(list(place_ids))}
        
        return [
            r.to_dict(users_map=users, places_map=places) 
            for r in reviews
        ]


@reviews_ns.route('/<string:review_id>')
@reviews_ns.param('review_id', 'The Review identifier (UUID)')
class ReviewResource(Resource):
    
    @reviews_ns.marshal_with(review_response_model)
    @reviews_ns.response(200, 'Review details retrieved successfully')
    @reviews_ns.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade_instance.get_review(review_id)
        if not review:
            reviews_ns.abort(404, 'Review not found')
            
        user_obj = facade_instance.get_user(review.user_id)
        place_obj = facade_instance.get_place(review.place_id)

        return review.to_dict(
            users_map={review.user_id: user_obj},
            places_map={review.place_id: place_obj}
        )

    @reviews_ns.expect(review_update_model, validate=True)
    @reviews_ns.response(200, 'Review updated successfully', review_response_model)
    @reviews_ns.response(404, 'Review not found')
    @reviews_ns.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        try:
            updated_review = facade_instance.update_review(review_id, reviews_ns.payload)
            if not updated_review:
                reviews_ns.abort(404, 'Review not found')

            user_obj = facade_instance.get_user(updated_review.user_id)
            place_obj = facade_instance.get_place(updated_review.place_id)

            return updated_review.to_dict(
                users_map={updated_review.user_id: user_obj},
                places_map={updated_review.place_id: place_obj}
            )

        except ValueError as e:
            reviews_ns.abort(400, str(e))
        except Exception as e:
            reviews_ns.abort(500, f"Internal error: {str(e)}")

    @reviews_ns.response(204, 'Review deleted successfully')
    @reviews_ns.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
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
        """Get all reviews for a specific place"""
        reviews_data = facade_instance.get_reviews_by_place(place_id)

        if reviews_data is None:
            reviews_ns.abort(404, 'Place not found')

        reviews = reviews_data if isinstance(reviews_data, list) else [reviews_data]

        user_ids = {r.user_id for r in reviews if r.user_id}

        users = {u.id: u for u in facade_instance.get_users_by_ids(list(user_ids))}
        place_obj = facade_instance.get_place(place_id)
        places = {place_id: place_obj} if place_obj else {}

        return [
            r.to_dict(users_map=users, places_map=places) 
            for r in reviews
        ]
