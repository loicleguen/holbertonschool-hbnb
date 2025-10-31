#!/usr/bin/python3
"""Amenity-specific repository for database operations"""

from app.models.amenity import Amenity
from app.persistence.repository import SQLAlchemyRepository


class AmenityRepository(SQLAlchemyRepository):
    """Repository for Amenity-specific database operations"""
    
    def __init__(self):
        """Initialize AmenityRepository with Amenity model"""
        super().__init__(Amenity)
    
    def get_amenity_by_name(self, name):
        """
        Get an amenity by name (Amenity-specific method)
        
        Args:
            name (str): Amenity name
            
        Returns:
            Amenity: Amenity object if found, None otherwise
        """
        return self.model.query.filter_by(name=name).first()