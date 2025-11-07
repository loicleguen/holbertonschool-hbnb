#!/usr/bin/python3
"""Facade pattern for HBnB application with SQLAlchemy"""

from app.persistence.user_repository import UserRepository
from app.persistence.amenity_repository import AmenityRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.review_repository import ReviewRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app import db


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.amenity_repo = AmenityRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()

    # ======================
    # ===== USERS =====
    # ======================

    def create_user(self, user_data):
        """Create a new user with SQLAlchemy"""
        email = user_data.get('email')
        if not email:
            raise ValueError("Email is required")
        
        if self.user_repo.get_user_by_email(email):
            raise ValueError("Email already registered")

        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def get_all_user(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        
        for field in ['id', 'created_at']:
            if field in data:
                raise ValueError(f"Cannot update '{field}'")
        
        if 'email' in data:
            existing_user = self.user_repo.get_user_by_email(data['email'])
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email already in use")
        
        if 'password' in data:
            user.hash_password(data['password'])
            data.pop('password')
        
        user.update(data)
        return user

    def delete_user(self, user_id):
        user = self.user_repo.get(user_id)
        if not user:
            return False
        
        # SQLAlchemy cascade will handle deletion of related places and reviews
        self.user_repo.delete(user_id)
        return True

    # ======================
    # ===== AMENITIES =====
    # ======================

    def create_amenity(self, amenity_data):
        """Create a new amenity with SQLAlchemy"""
        name = amenity_data.get("name")
        if not name:
            raise ValueError("Amenity name is required")
        
        # Check if amenity name already exists
        if self.amenity_repo.get_amenity_by_name(name):
            raise ValueError("Amenity name already exists")
        
        place_id = amenity_data.get("place_id")
        owner_id = amenity_data.get("owner_id")
        
        if place_id:
            place = self.place_repo.get(place_id)
            if not place:
                raise ValueError(f"Place with id '{place_id}' not found")
        
        if owner_id:
            owner = self.user_repo.get(owner_id)
            if not owner:
                raise ValueError(f"Owner with id '{owner_id}' not found")
        
        amenity = Amenity(
            name=name,
            place_id=place_id,
            owner_id=owner_id
        )
        
        self.amenity_repo.add(amenity)
        
        if place_id:
            place = self.place_repo.get(place_id)
            if place and amenity not in place.amenities:
                place.amenities.append(amenity)
                db.session.commit()
        
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        
        for field in ['id', 'created_at']:
            if field in amenity_data:
                raise ValueError(f"Cannot update '{field}'")
        
        if 'name' in amenity_data:
            existing = self.amenity_repo.get_amenity_by_name(amenity_data['name'])
            if existing and existing.id != amenity_id:
                raise ValueError("Amenity name already in use")
        
        old_place_id = amenity.place_id
        new_place_id = amenity_data.get('place_id')
        
        amenity.update(amenity_data)
        
        if new_place_id and new_place_id != old_place_id:
            if old_place_id:
                old_place = self.place_repo.get(old_place_id)
                if old_place and amenity in old_place.amenities:
                    old_place.amenities.remove(amenity)
            
            new_place = self.place_repo.get(new_place_id)
            if new_place and amenity not in new_place.amenities:
                new_place.amenities.append(amenity)
            
            db.session.commit()
        
        return amenity

    def delete_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return False
        
        if amenity.place_id:
            place = self.place_repo.get(amenity.place_id)
            if place and amenity in place.amenities:
                place.amenities.remove(amenity)
                db.session.commit()
        
        self.amenity_repo.delete(amenity_id)
        return True

    # ======================
    # ===== PLACES =====
    # ======================

    def create_place(self, place_data):
        """Create a new place with SQLAlchemy"""
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

        place = Place(
            title=place_data["title"],
            description=place_data.get("description", ""),
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner_id=owner.id,
            amenities=amenities
        )
        
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
        
        for field in ['id', 'owner_id', 'created_at']:
            if field in place_data:
                raise ValueError(f"Cannot update '{field}'")
        
        update_data = {}
        for key, value in place_data.items():
            if key == "amenities":
                new_amenities = []
                for a_id in value:
                    amenity = self.amenity_repo.get(a_id)
                    if not amenity:
                        raise ValueError(f"Amenity ID '{a_id}' not found")
                    new_amenities.append(amenity)
                update_data["amenities"] = new_amenities
            elif hasattr(place, key):
                update_data[key] = value

        place.update(update_data)
        return place

    def delete_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return False
        
        # SQLAlchemy cascade will handle deletion of related reviews
        self.place_repo.delete(place_id)
        return True

    # ======================
    # ===== REVIEWS =====
    # ======================
    
    def create_review(self, review_data):
        """Create a new review with SQLAlchemy"""
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')

        if not user_id or not self.user_repo.get(user_id):
            raise ValueError("Invalid or missing user_id")
        if not place_id or not self.place_repo.get(place_id):
            raise ValueError("Invalid or missing place_id")

        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        if not self.place_repo.get(place_id):
            return []
        return self.review_repo.get_reviews_by_place(place_id)

    def user_has_reviewed_place(self, user_id, place_id):
        reviews = self.get_reviews_by_place(place_id)
        for review in reviews:
            if review.user_id == user_id:
                return True
        return False

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        for field in ['id', 'user_id', 'place_id', 'created_at']:
            if field in review_data:
                raise ValueError(f"Cannot update '{field}'")
        
        review.update(review_data)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False
        return self.review_repo.delete(review_id)