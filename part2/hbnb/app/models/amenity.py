from .BaseModel import BaseModel, datetime

class Amenity(BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = kwargs.get("name", "")

    @property
    def validate(self):
        if not isinstance(self.id, str):
            raise TypeError("id must be a string")
        if len(self.id) < 1:
            raise ValueError("id mustn't be empty")
        if not isinstance(self.name, str):
            raise TypeError("name must be a string")
        if len(self.name) < 1 or len(self.name) > 50:
            raise ValueError("name must be between 1 and 50 characters")
        if not isinstance(self.created_at, datetime):
            raise TypeError("created_at must be a datetime")
        if not isinstance(self.updated_at, datetime):
            raise TypeError("updated_at must be a datetime")
