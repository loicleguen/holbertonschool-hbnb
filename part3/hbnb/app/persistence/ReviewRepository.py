#!/usr/bin/env python3
"""
Repository for Review entity, inheriting from the base Repository.
"""
from hbnb.app.persistence.repository import Repository
from hbnb.app.models.review import Review

class ReviewRepository(Repository):
    """
    Handles persistence operations for the Review model.
    Inherits generic CRUD from the base Repository class.
    """
    def __init__(self):
        """Initializes with the Review model."""
        super().__init__(Review)

# Note: All basic CRUD methods (save, get, get_all, update, delete) 
# are assumed to be implemented in the base Repository class (repository.py).
