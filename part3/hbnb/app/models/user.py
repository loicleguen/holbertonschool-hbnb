#!/usr/bin/python3
"""Defines the User model with SQLAlchemy"""

from app import db, bcrypt
from app.models.BaseModel import BaseModel
from sqlalchemy.orm import validates
from email_validator import validate_email, EmailNotValidError


class User(BaseModel):
    """User model mapped to database table"""
    
    __tablename__ = 'users'
    
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True) 
    password = db.Column(db.String(128), nullable=False) 
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name=None, last_name=None, email=None, password=None, is_admin=False, **kwargs):
        """Initialize User instance"""
        super().__init__(**kwargs)
        
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if email:
            self.email = email
        if is_admin is not None:
            self.is_admin = is_admin
        if password:
            self.hash_password(password)

    def hash_password(self, password):
        """Hashes the plaintext password using bcrypt and stores it."""
        if password:
            self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided plaintext password matches the stored hashed password."""
        if self.password is None:
            return False
        return bcrypt.check_password_hash(self.password, password)

    @validates('first_name')
    def validate_first_name(self, key, value):
        """Validate first_name"""
        if not value or not isinstance(value, str) or not value.strip():
            raise ValueError("first_name must be a non-empty string")
        if len(value) > 50:
            raise ValueError("first_name must be less than 50 characters")
        return value.strip()

    @validates('last_name')
    def validate_last_name(self, key, value):
        """Validate last_name"""
        if not value or not isinstance(value, str) or not value.strip():
            raise ValueError("last_name must be a non-empty string")
        if len(value) > 50:
            raise ValueError("last_name must be less than 50 characters")
        return value.strip()

    @validates('email')
    def validate_email_field(self, key, value):
        """Validate email format"""
        if not value or not isinstance(value, str):
            raise ValueError("Email must be a non-empty string")
        
        try:
            emailinfo = validate_email(value, check_deliverability=False)
            return emailinfo.normalized  # Normalize and return
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email: {str(e)}")

    def __repr__(self):
        return f"<User {self.email}>"

    def to_dict(self, include_relationships=False):
        """Returns a dictionary representation of the user, excluding the password hash."""
        data = super().to_dict(include_relationships)
        
        if 'password' in data:
            del data['password']
            
        return data