from .BaseModel import BaseModel, datetime
from .user import User
from .place import Place


class Review(BaseModel):
    def __init__(self, id: str, text: str, rating: int, place: str, user: str, created_at: datetime, updated_at: datetime):
        super().__init__()
        self.id = id
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
        self.created_at = created_at
        self.updated_at = updated_at


    @property
    def validate(self):
        if not isinstance(self.id, str):
            raise TypeError("id must be a string")
        if len(self.id) < 1:
            raise ValueError("id must be > 0")
        if not isinstance(self.text, str):
            raise TypeError("text must be a string")
        if len(self.text) < 1:
            raise ValueError("text mustn't empty")
        if not isinstance(self.rating, int):
            raise TypeError("rating must be a integer")
        if not 1 <= self.rating <= 5:
            raise ValueError("rating must be between 1 and 5 ")
        if not isinstance(self.place, Place):
            raise ValueError("place must be a place")
        if not isinstance(self.user, User):
            raise TypeError("user must be a user")
        if not isinstance(self.created_at, datetime):
            raise TypeError("created_at must be a datetime")
        if not isinstance(self.updated_at, datetime):
            raise TypeError("updated_at must be a datetime")