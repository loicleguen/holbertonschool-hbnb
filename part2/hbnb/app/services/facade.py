#!/usr/bin/python3
"""Facade layer: unified access to business logic"""

from app.persistence.repository import InMemoryRepository
from datetime import datetime
import uuid
from app.models.user import User
from app.models.amenity import Amenity


class HBnBFacade:
    """Facade for Users (part 2)"""

    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()


    # --- User methods ---
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
        if hasattr(user, "validate"):
            user.validate
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

        for field in ['id', 'email', 'created_at', 'updated_at']:
            if field in data:
                raise ValueError(f"Cannot update '{field}' via this endpoint")

        user.update(data)
        self.user_repo.update(user_id, data)
        return user


    # --- Amenity methods ---
    def create_amenity(self, amenity_data):
        name = amenity_data.get("name")
        if not name:
            raise ValueError("Amenity name is required")

        amenity = Amenity(name=name)
        amenity.id = str(uuid.uuid4())
        now = datetime.now()
        amenity.created_at = now
        amenity.updated_at = now

        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        if "name" in amenity_data:
            amenity.name = amenity_data["name"]
            amenity.updated_at = datetime.now()
        return amenity