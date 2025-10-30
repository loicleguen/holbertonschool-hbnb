#!/usr/bin/env python3
"""
SQLAlchemy model for the Review entity.
No relationships included yet, as per task instructions.
"""
from sqlalchemy import Column, String, Integer
from hbnb.app.models.BaseModel import db, BaseModel
from datetime import datetime
import uuid

class Review(BaseModel):
    """
    Review model that inherits from BaseModel and maps to the 'reviews' table.
    Includes core attributes as required by Task 07.
    """
    __tablename__ = 'reviews'

    # Core attributes as required by Task 07
    # Note: id, created_at, updated_at are inherited from BaseModel
    text = Column(String(1024), nullable=False)
    rating = Column(Integer, nullable=False) # Expected range 1-5, but no constraint added yet

    def __init__(self, text, rating, **kwargs):
        """Initializes a new Review instance."""
        super().__init__(**kwargs)
        self.text = text
        self.rating = rating

    def __repr__(self):
        return f"<Review id='{self.id}' rating='{self.rating}'>"

    def to_dict(self):
        """Returns a dictionary representation of the Review."""
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            'updated_at': self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at,
        }
