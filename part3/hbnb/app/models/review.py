#!/usr/bin/python3
"""Defines the Review model with SQLAlchemy"""

from app import db
from app.models.BaseModel import BaseModel
from sqlalchemy.orm import validates


class Review(BaseModel):
    """Review model mapped to database table"""
    
    __tablename__ = 'reviews'

    __table_args__ = (
        db.UniqueConstraint('user_id', 'place_id', name='unique_user_place_review'),
    )
    
    # SQLAlchemy columns
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    
    # Foreign keys (One-to-Many relationships)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False, index=True)
    
    # Relationships are defined via backref in User and Place models

    def __init__(self, place_id=None, user_id=None, text=None, rating=None, **kwargs):
        """Initialize Review instance"""
        super().__init__(**kwargs)
        if text:
            self.text = text
        if rating is not None:
            self.rating = rating
        if user_id:
            self.user_id = user_id
        if place_id:
            self.place_id = place_id

    @validates('text')
    def validate_text(self, key, value):
        """Validate review text"""
        if not value or not isinstance(value, str) or not value.strip():
            raise ValueError("text must be a non-empty string")
        return value.strip()

    @validates('rating')
    def validate_rating(self, key, value):
        """Validate rating (1-5)"""
        if not isinstance(value, int):
            raise TypeError("rating must be a number (integer or float)")
        if value < 1 or value > 5:
            raise ValueError("rating must be between 1 and 5")
        return value

    def to_dict(self, **kwargs):
        """
        Returns a dictionary representation of the Review
        
        All relationships (user, place) are loaded via SQLAlchemy
        """
        review_dict = super().to_dict(**kwargs)

        # ----- USER ----- (SQLAlchemy relationship)
        if hasattr(self, 'user') and self.user:
            review_dict['user'] = {
                'id': self.user.id,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name
            }
        else:
            review_dict['user'] = {
                'id': review_dict.get('user_id'),
                'first_name': None,
                'last_name': None
            }
        review_dict.pop('user_id', None)

        # ----- PLACE ----- (SQLAlchemy relationship)
        if hasattr(self, 'place') and self.place:
            review_dict['place'] = {
                'id': self.place.id,
                'title': self.place.title
            }
        else:
            review_dict['place'] = {
                'id': review_dict.get('place_id'),
                'title': None
            }
        review_dict.pop('place_id', None)

        return review_dict

    def __repr__(self):
        """String representation of Review"""
        return f"<Review {self.id} by User {self.user_id}>"