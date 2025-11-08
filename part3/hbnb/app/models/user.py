#!/usr/bin/python3
"""Defines the User model with SQLAlchemy"""

from app import db, bcrypt
from app.models.BaseModel import BaseModel
from sqlalchemy.orm import validates
from email_validator import validate_email, EmailNotValidError


class User(BaseModel):
    """User model mapped to database table"""
    
    __tablename__ = 'users'
    
    # SQLAlchemy columns
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    
    # Relationships
    places = db.relationship('Place', back_populates='owner', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy=True, cascade='all, delete-orphan')

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
        
        # Hash password if provided
        if password:
            self.hash_password(password)

    def hash_password(self, password):
        """Hash the password before storing it"""
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify the hashed password"""
        return bcrypt.check_password_hash(self.password, password)

    # SQLAlchemy validators
    @validates('first_name')
    def validate_first_name(self, key, value):
        """Validate first_name"""
        if not value or not isinstance(value, str) or not value.strip():
            raise ValueError("first_name must be a non-empty string")
        if len(value) > 255:
            raise ValueError("first_name must be less than 255 characters")
        return value.strip()

    @validates('last_name')
    def validate_last_name(self, key, value):
        """Validate last_name"""
        if not value or not isinstance(value, str) or not value.strip():
            raise ValueError("last_name must be a non-empty string")
        if len(value) > 255:
            raise ValueError("last_name must be less than 255 characters")
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

    def to_dict(self, **kwargs):
        """Return dictionary representation without password"""
        data = super().to_dict(**kwargs)
        # Never expose password in API responses
        data.pop('password', None)
        return data

    def __repr__(self):
        """String representation of User"""
        return f"<User {self.email}>"