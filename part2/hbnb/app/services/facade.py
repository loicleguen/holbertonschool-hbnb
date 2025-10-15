from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
import uuid
from datetime import datetime

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        email = user_data.get('email')
        if not email:
            raise ValueError("Email is required")
            
        existing_user = self.get_user_by_email(email)
        if existing_user:
            raise ValueError("Email already registered")

        now = datetime.now()

        full_user_data = user_data.copy()
        full_user_data.update({
            'id': str(uuid.uuid4()),      # Génère un ID unique
            'is_admin': False,            # Définit la valeur par défaut
            'created_at': now,            # Définit l'heure actuelle
            'updated_at': now,            # Définit l'heure actuelle
        })

        user = User(**full_user_data)
        
        return self.user_repo.add(user)

    def update_user(self, user_id, data):
        """Updates an existing User's attributes."""
        if not isinstance(user_id, str):
            raise TypeError("User ID must be a string")

        for field in ['id', 'email', 'created_at', 'updated_at']:
            if field in data:
                raise ValueError(f"Cannot update '{field}' via this endpoint")

        return self.user_repo.update(user_id, **data)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Retrieves a list of all User entities."""
        return self.user_repo.get_all()

    def create_amenity(self, amenity_data):
        """Creates and stores a new Amenity entity."""
        amenity = Amenity(**amenity_data)
        return self.amenity_repo.add(amenity)

    def get_amenity(self, amenity_id):
        """Retrieves an Amenity by ID."""
        if not isinstance(amenity_id, str):
            raise TypeError("Amenity ID must be a string")
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieves a list of all Amenity entities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Updates an existing Amenity's attributes."""
        if not isinstance(amenity_id, str):
            raise TypeError("Amenity ID must be a string")

        for field in ['id', 'created_at', 'updated_at']:
            if field in amenity_data:
                raise ValueError(f"Cannot update '{field}' via this endpoint")

        return self.amenity_repo.update(amenity_id, **amenity_data)

    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        pass
