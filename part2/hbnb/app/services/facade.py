from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Placeholder method for creating a user
    def create_user(self, user_data):
        # Logic will be implemented in later tasks
        user = User(**user_data)
        return self.user_repo.add(user)
    
    def get_user(self, user_id):
        return self.user_repo.get(user_id)
    
    def get_all_users(self):
        """Retrieves a list of all User entities."""
        return self.user_repository.get_all()
    
    def update_user(self, user_id, data):
        """Updates an existing User's attributes."""
        if not isinstance(user_id, str):
            raise TypeError("User ID must be a string")
        
        # Simple check to prevent updating core identity fields via PUT
        for field in ['id', 'email', 'created_at', 'updated_at']:
            if field in data:
                raise ValueError(f"Cannot update '{field}' via this endpoint")
        
        # Delegate to the repository's update method
        return self.user_repository.update(user_id, **data)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)


    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        pass