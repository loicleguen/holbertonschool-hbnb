from .BaseModel import BaseModel

class Amenity(BaseModel):
    def __init__(self, name=None, *args, **kwargs):
        # BaseModel handles id, created_at, updated_at, and deserializes kwargs
        super().__init__(*args, **kwargs) 
        
        if name is not None:
            self.name = name
        elif not hasattr(self, 'name'):
            self.name = kwargs.get("name", "")

    def validate(self):
        """Validates the Amenity object properties"""
        if not hasattr(self, 'name'):
            raise TypeError("name attribute is missing")
            
        if not isinstance(self.name, str):
            raise TypeError("Name must be a string")
        if len(self.name) < 1 or len(self.name) > 50:
            raise ValueError("Name must be between 1 and 50 characters")
        
        return True
