#!/usr/bin/python3
"""Defines the BaseModel class with SQLAlchemy"""

import uuid
from datetime import datetime
from app import db


class BaseModel(db.Model):
    """Base model with SQLAlchemy - shared by all entities"""
    
    __abstract__ = True  # This ensures SQLAlchemy does not create a table for BaseModel
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

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
        """Update instance attributes from dictionary"""
        for key, value in data.items():
            # Skip immutable and internal fields
            if key in ['id', 'created_at', '__class__']:
                continue
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def to_dict(self):
        """Return a dictionary representation of the instance."""
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        
        data['created_at'] = data['created_at'].isoformat() if isinstance(data['created_at'], datetime) else data['created_at']
        data['updated_at'] = data['updated_at'].isoformat() if isinstance(data['updated_at'], datetime) else data['updated_at']
        
        data.pop('password', None)
        return data

    def __repr__(self):
        """String representation of the instance"""
        return f"<{self.__class__.__name__} {self.id}>"
