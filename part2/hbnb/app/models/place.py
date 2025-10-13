from .BaseModel import BaseModel, datetime
from .user import User



class Place(BaseModel):
    def __init__(self, id: str, title: str, description: str, price: float, latitude: float, longitude: float, owner: str, created_at: datetime, updated_at: datetime):
        super().__init__()
        self.id = id
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.created_at = created_at
        self.updated_at = updated_at
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities


    def add_review(self, review):
        """Add a review to the place."""
        from .review import Review

        if not isinstance(review, Review):
            raise TypeError("review must be an instance of Review class")
        if review not in self.reviews:
            self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        from .amenity import Amenity

        if not isinstance(amenity, Amenity):
            raise TypeError("amenity must be an instance of Amenity class")
        if amenity not in self.amenities:
            self.amenities.append(amenity)


    @property
    def validate(self):
        if not isinstance(self.id, str):
            raise TypeError("id must be a string")
        if len(self.id) < 1:
            raise ValueError("id must be > 0")
        if not isinstance(self.title, str):
            raise TypeError("title must be a string")
        if not 1 > len(self.title) > 100:
            raise ValueError("title must be between 1 and 100 characters")
        if not isinstance(self.description, str):
            raise TypeError("description must be a string")
        if not isinstance(self.price, float):
            raise TypeError("price must be a float")
        if self.price < 0:
            raise ValueError("price must be positive")
        if not isinstance(self.latitude, float):
            raise TypeError("latitude must be a float")
        if not -90 <= self.latitude <= 90:
            raise ValueError("latitude Must be within the range of -90.0 to 90.0")
        if not isinstance(self.longitude, float):
            raise TypeError("longitude must be a float")
        if not -180 <= self.longitude <= 180:
            raise ValueError("longitude Must be within the range of -180.0 to 180.0")
        if not isinstance(self.owner, User):
            raise TypeError("owner must be a user")
        if not isinstance(self.created_at, datetime):
            raise TypeError("created_at must be a datetime")
        if not isinstance(self.updated_at, datetime):
            raise TypeError("updated_at must be a datetime")