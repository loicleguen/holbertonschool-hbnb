#!/usr/bin/python3
"""Defines the Amenity model with SQLAlchemy"""

from app import db
from app.models.BaseModel import BaseModel
from sqlalchemy.orm import validates


class Amenity(BaseModel):
    """Amenity model mapped to database table"""
    
    __tablename__ = 'amenities'
    
    # SQLAlchemy columns
    name = db.Column(db.String(255), nullable=False, unique=True)
    
    # Many-to-Many relationship with Place (will be activated after Place model)
    places = db.relationship('Place', secondary='place_amenity', back_populates='amenities', lazy='subquery')

    def __init__(self, name=None, place_id=None, owner_id=None, **kwargs):
        """Initialize Amenity instance"""
        super().__init__(**kwargs)
        if name:
            self.name = name
        
        self._temp_place_id = place_id
        self._temp_owner_id = owner_id

    @validates('name')
    def validate_name(self, key, value):
        """Validate amenity name"""
        if not value or not isinstance(value, str) or not value.strip():
            raise ValueError("Amenity name must be a non-empty string")
        if len(value) > 255:
            raise ValueError("Amenity name must be less than 255 characters")
        return value.strip()

    def to_dict(self, **kwargs):
        """Return dictionary representation of the amenity"""
        data = super().to_dict(**kwargs)
        
        if hasattr(self, '_temp_place_id') and self._temp_place_id:
            data['place_id'] = self._temp_place_id
        if hasattr(self, '_temp_owner_id') and self._temp_owner_id:
            data['owner_id'] = self._temp_owner_id
            
        return data

    def __repr__(self):
        """String representation of Amenity"""
        return f"<Amenity {self.name}>"