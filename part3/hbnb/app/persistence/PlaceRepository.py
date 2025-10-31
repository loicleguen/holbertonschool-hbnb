#!/usr/bin/env python3
"""
Repository for Place entity, inheriting from the base Repository.
"""
from hbnb.app.persistence.repository import Repository
from hbnb.app.models.place import Place

class PlaceRepository(Repository):
    """
    Handles persistence operations for the Place model.
    Inherits generic CRUD from the base Repository class.
    """
    def __init__(self):
        """Initializes with the Place model."""
        super().__init__(Place)

# Note: All basic CRUD methods (save, get, get_all, update, delete) 
# are assumed to be implemented in the base Repository class (repository.py).
