import uuid
from datetime import datetime

class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp



class User(BaseModel):
    def __init__(self, username, email):
        super().__init__()
        self.username = username
        self.email = email
        self.places = []  # List to store places owned by the user
        self.reviews = []  # List to store reviews written by the user
        self.amenities = []  # List to store amenities associated with the user

    def add_place(self, place):
        """Add a place to the user's list of places."""
        self.places.append(place)

    def add_review(self, review):
        """Add a review to the user's list of reviews."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the user's list of amenities."""
        self.amenities.append(amenity)



class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)


class Review(BaseModel):
    def __init__(self, text, user, place):
        super().__init__()
        self.text = text
        self.user = user  # Reference to the User who wrote the review
        self.place = place  # Reference to the Place being reviewed


class Amenity(BaseModel):
    def __init__(self, name, description):
        super().__init__()
        self.name = name
        self.description = description
        self.places = []  # List to store places associated with the amenity
