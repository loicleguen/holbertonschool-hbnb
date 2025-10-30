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

class AmenityRepository(SQLAlchemyRepository):
    """Specific repository for Amenity-related database operations."""
    def __init__(self):
        super().__init__(Amenity)
