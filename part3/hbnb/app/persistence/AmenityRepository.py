#!/usr/bin/env python3
"""
Repository for Amenity entity, inheriting from the base Repository.
"""
from hbnb.app.persistence.repository import Repository
from hbnb.app.models.amenity import Amenity

class AmenityRepository(Repository):
    """
    Handles persistence operations for the Amenity model.
    Inherits generic CRUD from the base Repository class.
    """
    def __init__(self):
        """Initializes with the Amenity model."""
        super().__init__(Amenity)

# Note: All basic CRUD methods (save, get, get_all, update, delete) 
# are assumed to be implemented in the base Repository class (repository.py).
