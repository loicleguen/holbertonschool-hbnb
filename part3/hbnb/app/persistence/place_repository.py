#!/usr/bin/python3
"""Place-specific repository for database operations"""

from app.models.place import Place
from app.persistence.repository import SQLAlchemyRepository


class PlaceRepository(SQLAlchemyRepository):
    """Repository for Place-specific database operations"""
    
    def __init__(self):
        """Initialize PlaceRepository with Place model"""
        super().__init__(Place)
    
    def get_places_by_owner(self, owner_id):
        """
        Get all places owned by a specific user
        
        Args:
            owner_id (str): User ID
            
        Returns:
            list: List of Place objects
        """
        return self.model.query.filter_by(owner_id=owner_id).all()