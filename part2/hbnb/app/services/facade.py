#!/usr/bin/python3
"""Facade layer: unified access to business logic"""

from app.persistence.repository import InMemoryRepository
from app.models.user import User
from datetime import datetime
import uuid

class HBnBFacade:
    """Facade for Users (part 2)"""

    def __init__(self):
        self.user_repo = InMemoryRepository()

    def create_user(self, user_data):
        """Create a new user with validation and defaults"""
        email = user_data.get('email')
        if not email:
            raise ValueError("Email is required")

        # Check if email already exists
        existing_user = self.get_user_by_email(email)
        if existing_user:
            raise ValueError("Email already registered")

        # Add default fields
        now = datetime.now()
        full_user_data = user_data.copy()
        full_user_data.update({
            'id': str(uuid.uuid4()),
            'created_at': now,
            'updated_at': now,
        })

        user = User(**full_user_data)
        # Validate user
        if hasattr(user, "validate"):
            user.validate
        # Add to repository
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve user by ID"""
        if not isinstance(user_id, str):
            raise TypeError("User ID must be a string")
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve user by email"""
        return self.user_repo.get_by_attribute('email', email)

    def get_all_user(self):
        """Retrieve all users"""
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        """Update an existing user's attributes"""
        user = self.user_repo.get(user_id)
        if not user:
            return None

        # Prevent updating protected fields
        for field in ['id', 'email', 'created_at', 'updated_at']:
            if field in data:
                raise ValueError(f"Cannot update '{field}' via this endpoint")

        # Apply update and validate
        user.update(data)
        self.user_repo.update(user_id, data)
        return user
