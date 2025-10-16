#!/usr/bin/python3
"""Defines the BaseModel class"""

import uuid
from datetime import datetime

class BaseModel:
    """Base class for all models, handling ID and timestamps"""

    def __init__(self, *args, **kwargs):
        """
        Initializes a new object or deserializes from kwargs.
        Kwargs are typically from the to_dict() method.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                # Deserialization: Convert string timestamps back to datetime objects
                if key in ('created_at', 'updated_at') and isinstance(value, str):
                    try:
                        value = datetime.fromisoformat(value)
                    except ValueError:
                        # Handle case where datetime string format is invalid
                        print(f"Warning: Could not deserialize datetime for key {key} with value {value}")
                        continue
                
                # Set attribute on the instance
                setattr(self, key, value)
        else:
            # New instance creation
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        """Returns the string representation of the object"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Update updated_at timestamp"""
        self.updated_at = datetime.now()

    def to_dict(self):
        """Return a dict representation"""
        result = self.__dict__.copy()
        result["__class__"] = self.__class__.__name__
        result["created_at"] = self.created_at.isoformat()
        result["updated_at"] = self.updated_at.isoformat()
        return result

    def update(self, data):
        """Update attributes from dict, protect immutable fields"""
        for key, value in data.items():
            if key in ['id', 'created_at']:
                continue
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
