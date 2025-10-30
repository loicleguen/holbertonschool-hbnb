from app.persistence.repository import UserRepository, PlaceRepository, ReviewRepository, AmenityRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    """
    The Facade pattern provides a simplified interface to the complex 
    logic of the business and persistence layers (Repositories).
    """

    def __init__(self):
        """Initializes all entity-specific repositories."""
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository() 
        self.review_repo = ReviewRepository() 
        self.amenity_repo = AmenityRepository() 
        
    # --- USER Operations ---

    def create_user(self, user_data):
        """Creates a new User instance and saves it via the repository."""
        
        if self.user_repo.get_user_by_email(user_data.get('email')):
            raise ValueError(f"User with email '{user_data.get('email')}' already exists.")

        password = user_data.pop('password')
        user = User(**user_data)
        user.hash_password(password)

        return self.user_repo.add(user)

    def get_user(self, user_id):
        """Retrieves a single User by ID."""
        return self.user_repo.get(user_id)
    
    def get_user_by_email(self, email):
        """Retrieves a single User by email using the specialized repository method."""
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        """Retrieves all Users."""
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        """Updates an existing User."""
        user = self.user_repo.get(user_id)
        if user is None:
            return None

        return self.user_repo.update(user, data)

    def delete_user(self, user_id):
        """Deletes a User by ID."""
        return self.user_repo.delete_by_id(user_id)

    # --- PLACE Operations ---

    def create_place(self, place_data):
        """Creates a new Place instance and saves it via the repository."""
        place = Place(**place_data)
        return self.place_repo.add(place)

    def get_place(self, place_id):
        """Retrieves a single Place by ID."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieves all Places."""
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        """Updates an existing Place."""
        place = self.place_repo.get(place_id)
        if place is None:
            return None
        return self.place_repo.update(place, data)

    def delete_place(self, place_id):
        """Deletes a Place by ID."""
        return self.place_repo.delete_by_id(place_id)

    # --- REVIEW Operations ---

    def create_review(self, review_data):
        """Creates a new Review instance and saves it via the repository."""
        review = Review(**review_data)
        return self.review_repo.add(review)

    def get_review(self, review_id):
        """Retrieves a single Review by ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieves all Reviews."""
        return self.review_repo.get_all()

    def update_review(self, review_id, data):
        """Updates an existing Review."""
        review = self.review_repo.get(review_id)
        if review is None:
            return None
        return self.review_repo.update(review, data)

    def delete_review(self, review_id):
        """Deletes a Review by ID."""
        return self.review_repo.delete_by_id(review_id)

    # --- AMENITY Operations ---

    def create_amenity(self, amenity_data):
        """Creates a new Amenity instance and saves it via the repository."""
        amenity = Amenity(**amenity_data)
        return self.amenity_repo.add(amenity)

    def get_amenity(self, amenity_id):
        """Retrieves a single Amenity by ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieves all Amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        """Updates an existing Amenity."""
        amenity = self.amenity_repo.get(amenity_id)
        if amenity is None:
            return None
        return self.amenity_repo.update(amenity, data)

    def delete_amenity(self, amenity_id):
        """Deletes an Amenity by ID."""
        return self.amenity_repo.delete_by_id(amenity_id)
