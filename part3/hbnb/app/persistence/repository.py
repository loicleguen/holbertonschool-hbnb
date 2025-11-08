#!/usr/bin/python3
"""Repository pattern with InMemoryRepository"""

from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        return next(
            (obj for obj in self._storage.values() if getattr(obj, attr_name, None) == attr_value),
            None
        )


# ========== AJOUTER CI-DESSOUS ==========

from app import db


class SQLAlchemyRepository(Repository):
    """Generic SQLAlchemy repository for database operations"""
    
    def __init__(self, model):
        """
        Initialize repository with a SQLAlchemy model
        
        Args:
            model: SQLAlchemy model class (e.g., User, Place, etc.)
        """
        self.model = model
    
    def add(self, obj):
        """Add object to database"""
        db.session.add(obj)
        db.session.commit()
        return obj
    
    def get(self, obj_id):
        """Get object by ID"""
        return self.model.query.get(obj_id)
    
    def get_all(self):
        """Get all objects"""
        return self.model.query.all()
    
    def update(self, obj_id, data):
        """Update object by ID"""
        obj = self.get(obj_id)
        if obj:
            obj.update(data)
            return obj
        return None
    
    def delete(self, obj_id):
        """Delete object by ID"""
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return True
        return False
    
    def get_by_attribute(self, attr_name, attr_value):
        """Get object by attribute (generic method)"""
        return self.model.query.filter_by(**{attr_name: attr_value}).first()