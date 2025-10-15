from .BaseModel import BaseModel, datetime


class Amenity(BaseModel):
    def __init__(self, id: str, name: str, created_at: datetime, updated_at: datetime):
        super().__init__()
        self.id = id
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at
        self.amenities = []  # List to store related amenities


    @property
    def validate(self):
        if not isinstance(self.id, str):
            raise TypeError("id must be a string")
        if len(self.id) < 1:
            raise ValueError("id mustn't empty")
        if not isinstance(self.name, str):
            raise TypeError("text must be a string")
        if 1 > len(self.name) > 50:
            raise ValueError("name must be between 1 and 50 characters")
        if not isinstance(self.created_at, datetime):
            raise TypeError("created_at must be a datetime")
        if not isinstance(self.updated_at, datetime):
            raise TypeError("updated_at must be a datetime")
