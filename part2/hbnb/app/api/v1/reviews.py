from flask_restx import Namespace, Resource, fields
from flask import request
from app import facade as facade_instance

reviewsns = Namespace('reviews', description='Review operations')


# -----------------------
# Models for Swagger
# -----------------------
review_place_nested_model = reviewsns.model('ReviewPlaceNested', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title of the place'),
})

review_user_nested_model = reviewsns.model('ReviewUserNested', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
})

review_model = reviewsns.model('ReviewInput', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Float(required=True, description='Rating of the place (1.0-5.0)'), 
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

review_response_model = reviewsns.model('ReviewResponse', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Float(description='Rating of the place (1.0-5.0)'),
    'user': fields.Nested(review_user_nested_model, description='User who wrote the review'),
    'place': fields.Nested(review_place_nested_model, description='Place being reviewed'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp'),
})

review_update_model = reviewsns.model('ReviewUpdate', {
    'text': fields.String(description='Text of the review'),
    'rating': fields.Float(description='Rating of the place (1.0-5.0)')
})


# -----------------------
# Routes
# -----------------------
@reviewsns.route('/')
class ReviewList(Resource):
    
    @reviewsns.expect(review_model, validate=True)
    @reviewsns.response(201, 'Review successfully created', review_response_model)
    @reviewsns.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        try:
            review = facade_instance.create_review(reviewsns.payload)
            
            user_obj = facade_instance.get_user(review.user_id)
            place_obj = facade_instance.get_place(review.place_id)
            
            return review.to_dict(
                users_map={review.user_id: user_obj},
                places_map={review.place_id: place_obj}
            ), 201
            
        except ValueError as e:
            reviewsns.abort(400, str(e))
        except Exception as e:
            reviewsns.abort(500, f"Internal error: {str(e)}")

    @reviewsns.marshal_list_with(review_response_model)
    @reviewsns.response(200, 'List of reviews retrieved successfully')
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


@reviewsns.route('/<string:review_id>')
@reviewsns.param('review_id', 'The Review identifier (UUID)')
class ReviewResource(Resource):
    
    @reviewsns.marshal_with(review_response_model)
    @reviewsns.response(200, 'Review details retrieved successfully')
    @reviewsns.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade_instance.get_review(review_id)
        if not review:
            reviewsns.abort(404, 'Review not found')
            
        user_obj = facade_instance.get_user(review.user_id)
        place_obj = facade_instance.get_place(review.place_id)

        return review.to_dict(
            users_map={review.user_id: user_obj},
            places_map={review.place_id: place_obj}
        )

    @reviewsns.expect(review_update_model, validate=True)
    @reviewsns.response(200, 'Review updated successfully', review_response_model)
    @reviewsns.response(404, 'Review not found')
    @reviewsns.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        try:
            updated_review = facade_instance.update_review(review_id, reviewsns.payload)
            if not updated_review:
                reviewsns.abort(404, 'Review not found')

            user_obj = facade_instance.get_user(updated_review.user_id)
            place_obj = facade_instance.get_place(updated_review.place_id)

            return updated_review.to_dict(
                users_map={updated_review.user_id: user_obj},
                places_map={updated_review.place_id: place_obj}
            )

        except ValueError as e:
            reviewsns.abort(400, str(e))
        except Exception as e:
            reviewsns.abort(500, f"Internal error: {str(e)}")

    @reviewsns.response(200, 'Review deleted successfully')
    @reviewsns.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        if facade_instance.delete_review(review_id):
            return {"message": "Review deleted successfully"}, 200
        reviewsns.abort(404, 'Review not found')


@reviewsns.route('/places/<string:place_id>/reviews')
@reviewsns.param('place_id', 'The Place identifier (UUID)')
class PlaceReviewList(Resource):

    @reviewsns.marshal_list_with(review_response_model)
    @reviewsns.response(200, 'List of reviews for the place retrieved successfully')
    @reviewsns.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade_instance.get_reviews_by_place(place_id)

        if reviews is None:
            reviewsns.abort(404, 'Place not found')

        user_ids = {r.user_id for r in reviews if r.user_id}
        
        users = {u.id: u for u in facade_instance.get_users_by_ids(list(user_ids))}
        place_obj = facade_instance.get_place(place_id)
        places = {place_id: place_obj} if place_obj else {}

        return [
            r.to_dict(users_map=users, places_map=places) 
            for r in reviews
        ]
