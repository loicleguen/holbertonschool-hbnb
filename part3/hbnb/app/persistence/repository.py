from app import db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class BaseRepository:
    """Base abstract class for repositories, defining the contract."""
    def get_all(self): raise NotImplementedError
    def get(self, entity_id): raise NotImplementedError
    def add(self, entity): raise NotImplementedError
    def update(self, entity, data): raise NotImplementedError
    def delete(self, entity): raise NotImplementedError

class SQLAlchemyRepository(BaseRepository):
    """
    Generic repository implementation using SQLAlchemy ORM.
    Handles basic CRUD operations using db.session.
    """
    def __init__(self, model):
        self.model = model

    def get_all(self):
        """Returns all instances of the model."""
        return self.model.query.all()

    def get(self, entity_id):
        """Returns a single instance by its ID."""
        return self.model.query.get(entity_id)

    def add(self, entity):
        """Adds a new entity to the database session and commits."""
        db.session.add(entity)
        db.session.commit()
        return entity

    def update(self, entity, data):
        """
        Updates an existing entity with new data and commits.
        NOTE: 'entity' must be a retrieved SQLAlchemy object.
        """
        for key, value in data.items():
            if key in ('id', 'created_at', 'updated_at') or (key == 'password' and not value):
                continue
            
            if hasattr(entity, key):
                if key == 'password' and isinstance(entity, User):
                    entity.hash_password(value)
                else:
                    setattr(entity, key, value)

        db.session.commit()
        return entity

    def delete(self, entity):
        """Deletes an entity from the database session and commits."""
        db.session.delete(entity)
        db.session.commit()
        return True

    def delete_by_id(self, entity_id):
        """Deletes an entity by its ID."""
        entity = self.get(entity_id)
        if entity:
            return self.delete(entity)
        return False


# --- Entity Specific Repositories ---

class UserRepository(SQLAlchemyRepository):
    """
    Specific repository for User-related database operations.
    Extends generic SQLAlchemyRepository with domain-specific queries.
    """
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        """Retrieves a user instance by their email address."""
        return self.model.query.filter_by(email=email).first()
        
class PlaceRepository(SQLAlchemyRepository):
    """Specific repository for Place-related database operations."""
    def __init__(self):
        super().__init__(Place)

class ReviewRepository(SQLAlchemyRepository):
    """Specific repository for Review-related database operations."""
    def __init__(self):
        super().__init__(Review)

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
