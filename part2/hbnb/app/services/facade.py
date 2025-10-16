from app.persistence.repository import InMemoryRepository
from datetime import datetime
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # --- Users ---

    def create_user(self, user_data):
        email = user_data.get('email')
        if not email:
            raise ValueError("Email is required")
        if self.get_user_by_email(email):
            raise ValueError("Email already registered")


        user = User()
        for k, v in user_data.items():
            setattr(user, k, v)
        if hasattr(user, "validate"):
            user.validate()
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_user(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        for field in ['id', 'email', 'created_at', 'updated_at']:
            if field in data:
                raise ValueError(f"Cannot update '{field}'")
        user.update(data)
        return user


    # --- Amenities ---
    def create_amenity(self, amenity_data):
        name = amenity_data.get("name")
        if not name:
            raise ValueError("Amenity name is required")
        amenity = Amenity()
        amenity.name = name
        amenity.validate()
        self.amenity_repo.add(amenity)
        return amenity


    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        if "name" in amenity_data:
            amenity.name = amenity_data["name"]
            amenity.updated_at = datetime.now()
        return amenity

    # --- Places ---
    def create_place(self, place_data):
        owner = self.user_repo.get(place_data.get("owner_id"))
        if not owner:
            raise ValueError("Owner not found")
        place = Place(
            title=place_data["title"],
            description=place_data.get("description", ""),
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner_id=owner.id,
            amenities=[]
        )
        for a_id in place_data.get("amenities", []):
            amenity = self.amenity_repo.get(a_id)
            if not amenity:
                raise ValueError(f"Amenity {a_id} not found")
            place.add_amenity(a_id)
        place.validate()
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        for key, value in place_data.items():
            if key in ['id', 'owner_id', 'created_at']:
                raise ValueError(f"Cannot update '{key}'")
            if key == "amenities":
                for a_id in value:
                    if not self.amenity_repo.get(a_id):
                        raise ValueError(f"Amenity {a_id} not found")
                place.amenities = value
            elif hasattr(place, key):
                setattr(place, key, value)
        place.validate()
        return place

    # --- Review ---
    
    def create_review(self, review_data):
        """
        Creates and stores a new Review entity.
        Validates foreign keys (user_id, place_id).
        """
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')

        if not user_id or not self.user_repo.get(user_id):
            raise ValueError("Invalid or missing user_id.")
        if not place_id or not self.place_repo.get(place_id):
            raise ValueError("Invalid or missing place_id.")

        review = Review()
        for k, v in review_data.items():
            setattr(review, k, v)

        review.validate()

        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Retrieves a Review by ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieves a list of all Review entities."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Retrieves all reviews associated with a specific Place ID."""
        if not self.place_repo.get(place_id):
             return None 

        return self.review_repo.get_by_attribute('place_id', place_id)

    def update_review(self, review_id, review_data):
        """
        Updates an existing Review's attributes.
        Only 'text' and 'rating' should be updateable.
        """
        review = self.review_repo.get(review_id)
        if not review:
            return None

        for field in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            if field in review_data:
                raise ValueError(f"Cannot update '{field}'")

        for key, value in review_data.items():
            setattr(review, key, value)

        review.validate()
        review.updated_at = datetime.now()

        return review

    def delete_review(self, review_id):
        """Deletes a Review by ID."""
        return self.review_repo.delete(review_id)
