#!/usr/bin/python3
"""User-specific repository for database operations"""

from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    """Repository for User-specific database operations"""
    
    def __init__(self):
        """Initialize UserRepository with User model"""
        super().__init__(User)
    
    def get_user_by_email(self, email):
        """
        Get a user by email address (User-specific method)
        
        Args:
            email (str): User's email address
            
        Returns:
            User: User object if found, None otherwise
        """
        return self.model.query.filter_by(email=email).first()
    
    def get_user_by_attribute(self, attr_name, attr_value):
        """
        Get a user by any attribute (backward compatibility)
        
        Args:
            attr_name (str): Attribute name (e.g., 'first_name')
            attr_value: Attribute value
            
        Returns:
            User: User object if found, None otherwise
        """
        return self.model.query.filter_by(**{attr_name: attr_value}).first()