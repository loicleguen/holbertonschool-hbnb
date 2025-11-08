#!/usr/bin/python3
"""Review-specific repository for database operations"""

from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository


class ReviewRepository(SQLAlchemyRepository):
    """Repository for Review-specific database operations"""
    
    def __init__(self):
        """Initialize ReviewRepository with Review model"""
        super().__init__(Review)
    
    def get_reviews_by_place(self, place_id):
        """
        Get all reviews for a specific place
        
        Args:
            place_id (str): Place ID
            
        Returns:
            list: List of Review objects
        """
        return self.model.query.filter_by(place_id=place_id).all()
    
    def get_reviews_by_user(self, user_id):
        """
        Get all reviews written by a specific user
        
        Args:
            user_id (str): User ID
            
        Returns:
            list: List of Review objects
        """
        return self.model.query.filter_by(user_id=user_id).all()