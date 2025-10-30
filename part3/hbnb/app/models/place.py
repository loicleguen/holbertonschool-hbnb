#!/usr/bin/env python3
"""
SQLAlchemy model for the Place entity.
No relationships included yet, as per task instructions.
"""
from sqlalchemy import Column, String, Float, Integer
from hbnb.app.models.BaseModel import db, BaseModel
from datetime import datetime
import uuid

class Place(BaseModel):
    """
    Place model that inherits from BaseModel and maps to the 'places' table.
    Includes core attributes as required by Task 07.
    """
    __tablename__ = 'places'

    # Core attributes as required by Task 07
    # Note: id, created_at, updated_at are inherited from BaseModel
    title = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    price = Column(Float, nullable=False, default=0.0)
    latitude = Column(Float, nullable=False, default=0.0)
    longitude = Column(Float, nullable=False, default=0.0)
    # Added max_guests as it is a common place attribute and was in the ERD context.
    max_guests = Column(Integer, nullable=False, default=1)
    
    def __init__(self, title, description=None, price=0.0, latitude=0.0, longitude=0.0, max_guests=1, **kwargs):
        """Initializes a new Place instance."""
        super().__init__(**kwargs)
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.max_guests = max_guests

    def __repr__(self):
        return f"<Place id='{self.id}' title='{self.title}'>"

    def to_dict(self):
        """Returns a dictionary representation of the Place."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'max_guests': self.max_guests,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            'updated_at': self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at,
        }
