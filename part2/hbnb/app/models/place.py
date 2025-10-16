from .BaseModel import BaseModel


class Place(BaseModel):
    def __init__(self, title=None, description=None, price=None,
                 latitude=None, longitude=None, owner_id=None,
                 amenities=None, *args, **kwargs):

        super().__init__(*args, **kwargs)

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
        if amenity_id not in self.amenities:
            self.amenities.append(amenity_id)

    def to_dict(self, owners_map=None, amenities_map=None, reviews_map=None, **kwargs):
        """
        Returns a dictionary representation of the Place, including nested objects,
        and absorbing any extra arguments like 'safe'.
        """
        place_dict = super().to_dict(**kwargs) 

        owner_id = place_dict.pop('owner_id', None)
        if owner_id and owners_map and owner_id in owners_map:
            owner_obj = owners_map[owner_id]
            place_dict['owner'] = owner_obj.to_dict(safe=True) 
        else:
            place_dict['owner'] = {'id': owner_id, 'first_name': None, 'last_name': None, 'email': None}

        amenity_ids = place_dict.pop('amenities', [])
        if amenities_map and amenity_ids:
            place_dict['amenities'] = [
                amenities_map[a_id].to_dict()
                for a_id in amenity_ids if a_id in amenities_map
            ]
        else:
             place_dict['amenities'] = []

        place_dict['reviews'] = [r.to_dict() for r in reviews_map] if reviews_map else []


        return place_dict
