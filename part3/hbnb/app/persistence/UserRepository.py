# FILE: part3/hbnb/app/persistence/user_repository.py

from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository # <--- MODIFICATION: New base class

class UserRepository(SQLAlchemyRepository):
    """Repository for User-specific database operations"""

    def __init__(self):
        """Initialize UserRepository with User model"""
        super().__init__(User)

    def get_user_by_email(self, email):
        """ Get a user by their email (User-specific method) """
        return self.model.query.filter_by(email=email).first()