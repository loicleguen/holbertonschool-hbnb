from .BaseModel import BaseModel, datetime


class Place(BaseModel):
    # This __init__ is now robust for both creation (positional or kwargs) and loading (kwargs)
    def __init__(self, title=None, description=None, price=None,
                 latitude=None, longitude=None, owner_id=None,
                 amenities=None, *args, **kwargs):
        
        # Pass all args to BaseModel to handle ID/timestamps/deserialization
        super().__init__(*args, **kwargs)
        
        # If loading from kwargs, BaseModel already sets attributes via setattr.
        # We ensure attributes are set for new objects (positional args) or fallback to kwargs values.
        self.title = self.__dict__.get('title', title)
        self.description = self.__dict__.get('description', description)
        self.price = self.__dict__.get('price', price)
        self.latitude = self.__dict__.get('latitude', latitude)
        self.longitude = self.__dict__.get('longitude', longitude)
        self.owner_id = self.__dict__.get('owner_id', owner_id)
        self.amenities = self.__dict__.get('amenities', amenities or [])

    def validate(self):
        """Validate Place attributes"""
        
        if not hasattr(self, 'title') or not isinstance(self.title, str) or not (1 <= len(self.title) <= 100):
            raise ValueError("title must be a string between 1 and 100 characters")
            
        if hasattr(self, 'description') and self.description is not None and not isinstance(self.description, str):
            raise TypeError("Description must be a string or None")
            
        if not hasattr(self, 'price') or not isinstance(self.price, (float, int)):
            raise TypeError("Price must be a float or int")
        if self.price is not None and self.price < 0:
            raise ValueError("Price must be non-negative")
            
        if not hasattr(self, 'latitude') or not isinstance(self.latitude, (float, int)):
            raise TypeError("Latitude must be a float or int")
        if self.latitude is not None and not -90 <= self.latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90")
            
        if not hasattr(self, 'longitude') or not isinstance(self.longitude, (float, int)):
            raise TypeError("Longitude must be a float or int")
        if self.longitude is not None and not -180 <= self.longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180")
            
        if not hasattr(self, 'owner_id') or not isinstance(self.owner_id, str) or not self.owner_id:
            raise TypeError("owner_id must be a non-empty string")
            
        if not hasattr(self, 'amenities') or not isinstance(self.amenities, list):
            raise TypeError("amenities must be a list")
        
        return True

    def add_amenity(self, amenity_id):
        # This function might need adjustment depending on whether it stores IDs or objects
        if amenity_id not in self.amenities:
            self.amenities.append(amenity_id)

    def to_dict(self, owners_map=None, amenities_map=None):
        """
        Serialize Place object to a dict for API responses.
        owners_map: dict {owner_id: owner_obj}
        amenities_map: dict {amenity_id: amenity_obj}
        """
        owner_obj = None
        if owners_map and self.owner_id in owners_map:
            owner_obj = owners_map[self.owner_id]

        # Amenities List preparation
        amenities_list = []
        if self.amenities:
            # If the amenities list already contains full objects (as set by Facade.create_place), use them.
            if self.amenities and hasattr(self.amenities[0], 'name'):
                 amenities_list = self.amenities
            elif amenities_map:
                # If only IDs are stored, use the map
                amenities_list = [amenities_map[aid] for aid in self.amenities if aid in amenities_map and hasattr(amenities_map[aid], 'id')]
            else:
                # Fallback, this will likely cause marshalling errors if full objects are expected
                pass 

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": float(self.price),
            "latitude": float(self.latitude),
            "longitude": float(self.longitude),
            "owner": {
                "id": owner_obj.id,
                "first_name": owner_obj.first_name,
                "last_name": owner_obj.last_name,
                "email": owner_obj.email
            } if owner_obj and hasattr(owner_obj, 'email') else None,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else str(self.created_at),
            "updated_at": self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else str(self.updated_at),
            "amenities": [
                {"id": a.id, "name": a.name} for a in amenities_list if hasattr(a, 'id') and hasattr(a, 'name')
            ]
        }
