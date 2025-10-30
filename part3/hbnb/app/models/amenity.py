#!/usr/bin/env python3
"""
SQLAlchemy model for the Amenity entity.
No relationships included yet, as per task instructions.
"""
from sqlalchemy import Column, String
from hbnb.app.models.BaseModel import db, BaseModel
from datetime import datetime
import uuid

class Amenity(BaseModel):
    """
    Amenity model that inherits from BaseModel and maps to the 'amenities' table.
    Includes core attributes as required by Task 07.
    """
    __tablename__ = 'amenities'

    # Core attributes as required by Task 07
    # Note: id, created_at, updated_at are inherited from BaseModel
    name = Column(String(128), nullable=False, unique=True) # Amenity names should typically be unique

    def __init__(self, name, **kwargs):
        """Initializes a new Amenity instance."""
        super().__init__(**kwargs)
        self.name = name

    def __repr__(self):
        return f"<Amenity id='{self.id}' name='{self.name}'>"

    def to_dict(self):
        """Returns a dictionary representation of the Amenity."""
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            'updated_at': self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at,
        }
