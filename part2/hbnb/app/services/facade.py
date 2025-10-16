from app.persistence.repository import InMemoryRepository
from datetime import datetime
import uuid
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
        
        # KEY FIX: Call save() to run validation (password hashing removed from User.save())
        user.save() 
        
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_users_by_ids(self, user_ids):
        """Helper to retrieve a list of user objects by their IDs."""
        return [self.get_user(uid) for uid in user_ids if self.get_user(uid)]

    def get_all_user(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        for field in ['id', 'email', 'created_at']: # updated_at must be updated by save()
            if field in data:
                raise ValueError(f"Cannot update '{field}'")
        user.update(data) # user.update() calls user.save() internally
        return user

    def delete_user(self, user_id):
        """Delete a user and their associated places (cascade-like logic)"""
        user = self.user_repo.get(user_id)
        if not user:
            return False

        # Find and delete all places owned by this user
        places_to_delete = [
            place.id for place in self.place_repo.get_all() 
            if place.owner_id == user_id
        ]
        for place_id in places_to_delete:
            self.place_repo.delete(place_id) 

        self.user_repo.delete(user_id)
        return True

    # --- Amenities ---
    def create_amenity(self, amenity_data):
        name = amenity_data.get("name")
        if not name:
            raise ValueError("Amenity name is required")
        
        # Pass kwargs to constructor for proper BaseModel initialization
        amenity = Amenity(name=name) 
        amenity.validate()
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self,):
        return self.amenity_repo.get_all()
    
    def get_amenities_by_ids(self, amenity_ids):
        """Helper to retrieve a list of amenity objects by their IDs."""
        return [self.get_amenity(aid) for aid in amenity_ids if self.get_amenity(aid)]

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        if "name" in amenity_data:
            amenity.name = amenity_data["name"]
            amenity.save() # Use save() to update updated_at and validate
        return amenity

    def delete_amenity(self, amenity_id):
        """Delete an amenity and update places that might reference it."""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return False

        # Update all places to remove this amenity from their list
        for place in self.place_repo.get_all():
            # Ensure the list contains objects before checking
            if isinstance(place.amenities, list) and place.amenities and hasattr(place.amenities[0], 'id'):
                # Filter out the amenity object by its ID
                original_length = len(place.amenities)
                place.amenities = [a for a in place.amenities if a.id != amenity_id]
                
                # If the list changed, save the place
                if len(place.amenities) < original_length:
                    place.save()
        
        self.amenity_repo.delete(amenity_id)
        return True

    # --- Places ---
    def create_place(self, place_data):
        owner = self.user_repo.get(place_data.get("owner_id"))
        if not owner:
            raise ValueError("Owner not found")

        # Retrieve amenity objects from IDs
        amenity_ids = place_data.get("amenities", [])
        amenities = []
        if amenity_ids:
            for a_id in amenity_ids:
                amenity = self.amenity_repo.get(a_id)
                if not amenity:
                    raise ValueError(f"Amenity ID '{a_id}' not found")
                amenities.append(amenity)

        # Use kwargs for deserialization robustness in Place model
        place_kwargs = {
            "title": place_data["title"],
            "description": place_data.get("description", ""),
            "price": place_data["price"],
            "latitude": place_data["latitude"],
            "longitude": place_data["longitude"],
            "owner_id": owner.id,
            "amenities": amenities # Pass objects, not IDs
        }
        
        # Place constructor now handles validation and BaseModel initialization
        place = Place(**place_kwargs) 
        
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
        
        update_data = {}
        
        for key, value in place_data.items():
            if key in ['id', 'owner_id', 'created_at']:
                raise ValueError(f"Cannot update '{key}'")
            
            if key == "amenities":
                # Convert amenity IDs to objects for the Place model
                new_amenities = []
                for a_id in value:
                    amenity = self.amenity_repo.get(a_id)
                    if not amenity:
                        raise ValueError(f"Amenity ID '{a_id}' not found")
                    new_amenities.append(amenity)
                update_data["amenities"] = new_amenities
            elif hasattr(place, key):
                update_data[key] = value

        # Update the place object using the update method (which handles validation and save)
        place.update(update_data) 
        return place

    def delete_place(self, place_id):
        """Delete a place."""
        place = self.place_repo.get(place_id)
        if not place:
            return False
        
        self.place_repo.delete(place_id)
        return True

    def get_places_by_ids(self, place_ids):
        """Helper to retrieve a list of place objects by their IDs."""
        return [self.get_place(pid) for pid in place_ids if self.get_place(pid)]

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

        review = Review(**review_data)
        
        review.save() 
        
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

        for field in ['id', 'user_id', 'place_id', 'created_at']:
            if field in review_data:
                raise ValueError(f"Cannot update '{field}'")
        
        review.update(review_data) 

        return review

    def delete_review(self, review_id):
        """Deletes a Review by ID."""
        return self.review_repo.delete(review_id)
