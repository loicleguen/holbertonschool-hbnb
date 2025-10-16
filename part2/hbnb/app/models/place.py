from .BaseModel import BaseModel, datetime
import uuid

class Place(BaseModel):
    def __init__(self, title: str, description: str, price: float,
                 latitude: float, longitude: float, owner_id: str,
                 amenities=None):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.amenities = amenities or []

        self.validate()

    def validate(self):
        if not isinstance(self.title, str) or not (1 <= len(self.title) <= 100):
            raise ValueError("title must be a string between 1 and 100 characters")
        if self.description is not None and not isinstance(self.description, str):
            raise TypeError("Description must be a string")
        if not isinstance(self.price, (float, int)):
            raise TypeError("Price must be a float or int")
        if self.price < 0:
            raise ValueError("Price must be non-negative")
        if not isinstance(self.latitude, (float, int)):
            raise TypeError("Latitude must be a float")
        if not -90 <= self.latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        if not isinstance(self.longitude, (float, int)):
            raise TypeError("Longitude must be a float")
        if not -180 <= self.longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        if not isinstance(self.owner_id, str):
            raise TypeError("owner_id must be a string")
        if not isinstance(self.amenities, list):
            raise TypeError("amenities must be a list")

    def add_amenity(self, amenity_id: str):
        if amenity_id not in self.amenities:
            self.amenities.append(amenity_id)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "amenities": self.amenities,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
