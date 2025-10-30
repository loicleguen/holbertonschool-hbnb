from .BaseModel import BaseModel

class Amenity(BaseModel):
    # Class attributes
    name = ""
    place_id = None  # ID of the place this amenity belongs to
    owner_id = None  # ID of the place owner who created this amenity
    
    def __init__(self, name=None, place_id=None, owner_id=None, *args, **kwargs):
        # BaseModel handles id, created_at, updated_at, and deserializes kwargs
        super().__init__(*args, **kwargs) 
        
        # Set name
        if name is not None:
            self.name = name
        elif not hasattr(self, 'name'):
            self.name = kwargs.get("name", "")
        
        # Set place_id
        if place_id is not None:
            self.place_id = place_id
        elif not hasattr(self, 'place_id'):
            self.place_id = kwargs.get("place_id", None)
        
        # Set owner_id
        if owner_id is not None:
            self.owner_id = owner_id
        elif not hasattr(self, 'owner_id'):
            self.owner_id = kwargs.get("owner_id", None)

    def validate(self):
        """Validates the Amenity object properties"""
        if not hasattr(self, 'name'):
            raise TypeError("name attribute is missing")
            
        if not isinstance(self.name, str):
            raise TypeError("Name must be a string")
        if len(self.name) < 1 or len(self.name) > 50:
            raise ValueError("Name must be between 1 and 50 characters")
        
        # Validate place_id
        if not hasattr(self, 'place_id') or not self.place_id:
            raise ValueError("place_id is required")
        
        if not isinstance(self.place_id, str):
            raise TypeError("place_id must be a string")
        
        # Validate owner_id
        if not hasattr(self, 'owner_id') or not self.owner_id:
            raise ValueError("owner_id is required")
        
        if not isinstance(self.owner_id, str):
            raise TypeError("owner_id must be a string")
        
        return True

    def save(self):
        """Save the amenity after validation"""
        self.validate()
        super().save()

    def update(self, data):
        """Update amenity attributes with provided data"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.validate()
        super().save()

    def to_dict(self):
        """Return dictionary representation of the amenity"""
        data = super().to_dict()
        if self.place_id:
            data['place_id'] = self.place_id
        if self.owner_id:
            data['owner_id'] = self.owner_id
        return data