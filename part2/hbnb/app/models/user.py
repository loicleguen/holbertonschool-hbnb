#!/usr/bin/python3
"""Defines the User class"""

from app.models.BaseModel import BaseModel
from email_validator import validate_email, EmailNotValidError


class User(BaseModel):
    """Representation of a user"""

    email = ""
    password = ""
    first_name = ""
    last_name = ""

    @property
    def validate(self):
        """Validate user data"""
        # First name
        if not isinstance(self.first_name, str) or not self.first_name.strip():
            raise ValueError("first_name must be a non-empty string")
        if len(self.first_name) > 50:
            raise ValueError("first_name must be less than 50 characters")

        # Last name
        if not isinstance(self.last_name, str) or not self.last_name.strip():
            raise ValueError("last_name must be a non-empty string")
        if len(self.last_name) > 50:
            raise ValueError("last_name must be less than 50 characters")

        # Email
        try:
            emailinfo = validate_email(self.email, check_deliverability=False)
            self.email = emailinfo.normalized
        except EmailNotValidError as e:
            raise ValueError(str(e))

        # Password
        if not isinstance(self.password, str):
            raise TypeError("password must be a string")
        if len(self.password) < 6:
            raise ValueError("password must be at least 6 characters long")

        return True

    def save(self):
        """Override save to validate before saving"""
        self.validate  # Validate all fields
        super().save()  # Call BaseModel save() to update timestamp

    def update(self, data):
        """Override update to apply changes and validate"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.validate  # Validate after update
        super().save()  # Save updated object
