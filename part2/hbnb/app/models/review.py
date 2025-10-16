from .BaseModel import BaseModel, datetime


class Review(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = kwargs.get('text', '')
        self.rating = kwargs.get('rating', 0)
        self.place_id = kwargs.get('place_id', '')
        self.user_id = kwargs.get('user_id', '')


    def validate(self):

        if not isinstance(self.id, str) or len(self.id) < 1:
            raise ValueError("ID is invalid or missing.")

        if not isinstance(self.text, str) or len(self.text) < 1:
            raise ValueError("Text must be a non-empty string.")

        if not isinstance(self.rating, int) or not (1 <= self.rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5.")

        if not isinstance(self.place_id, str) or len(self.place_id) < 1:
            raise ValueError("place_id must be a non-empty string.")

        if not isinstance(self.user_id, str) or len(self.user_id) < 1:
            raise ValueError("user_id must be a non-empty string.")
