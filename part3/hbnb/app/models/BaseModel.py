#!/usr/bin/python3
"""Defines the BaseModel class with SQLAlchemy support"""

import uuid
from datetime import datetime, timezone
from app import db


class BaseModel(db.Model):
    """Base class for all models, handling ID and timestamps with SQLAlchemy"""
    
    __abstract__ = True  # This ensures SQLAlchemy does not create a table for BaseModel
    
    # SQLAlchemy columns
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, 
                           default=lambda: datetime.now(timezone.utc), 
                           onupdate=lambda: datetime.now(timezone.utc))

    def __init__(self, *args, **kwargs):
        """
        Initializes a new object or deserializes from kwargs.
        SQLAlchemy will handle id, created_at, updated_at automatically if not provided.
        """
        super().__init__(*args, **kwargs)
        
        # Only set id, created_at, updated_at if not already set by SQLAlchemy
        if not hasattr(self, 'id') or self.id is None:
            self.id = str(uuid.uuid4())
        if not hasattr(self, 'created_at') or self.created_at is None:
            self.created_at = datetime.utcnow()
        if not hasattr(self, 'updated_at') or self.updated_at is None:
            self.updated_at = datetime.utcnow()

    def __repr__(self):
        """Returns a string representation of the object."""
        return f"<{self.__class__.__name__} {self.id}>"

    def save(self):
        """Save the current instance to the database"""
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the current instance from the database"""
        db.session.delete(self)
        db.session.commit()

    def update(self, data):
        """Update attributes from dict, protect immutable fields"""
        for key, value in data.items():
            if key in ['id', 'created_at', '__class__']:
                continue  # Skip immutable fields
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def to_dict(self, include_relationships=False):
        """Returns a dictionary representation of the instance for JSON serialization."""
        data = {}
        
        for column in self.__table__.columns:
            key = column.name
            value = getattr(self, key)
            
            if isinstance(value, datetime):
                data[key] = value.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')
            else:
                data[key] = value
            
        data['__class__'] = self.__class__.__name__
        
        return data
