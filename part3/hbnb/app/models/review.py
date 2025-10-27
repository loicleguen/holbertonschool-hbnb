from .BaseModel import BaseModel

class Review(BaseModel):
    def __init__(self, place_id=None, user_id=None, text=None, rating=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.place_id = self.__dict__.get('place_id', place_id) 
        self.user_id = self.__dict__.get('user_id', user_id) 
        self.text = self.__dict__.get('text', text)
        self.rating = self.__dict__.get('rating', rating)

    def validate(self):
        if not hasattr(self, 'text') or not isinstance(self.text, str) or len(self.text) < 1:
            raise ValueError("text must be a non-empty string")
        

        if not hasattr(self, 'rating') or not isinstance(self.rating, (int, float)):
            raise TypeError("rating must be a number (integer or float)")


        if not 1 <= self.rating <= 5:
            raise ValueError("rating must be between 1 and 5 ")

        if not hasattr(self, 'place_id') or not isinstance(self.place_id, str) or not self.place_id:
            raise ValueError("place_id must be a non-empty string ID")
        if not hasattr(self, 'user_id') or not isinstance(self.user_id, str) or not self.user_id: 
            raise TypeError("user_id must be a non-empty string ID")
        return True

    def to_dict(self, users_map=None, places_map=None, **kwargs):
        """
        Returns a dictionary representation of the Review, including nested 'user' and 'place' objects if maps are provided.
        """
        review_dict = super().to_dict(**kwargs) 

        user_id = review_dict.pop('user_id', None)
        if user_id and users_map and user_id in users_map:
            user_obj = users_map[user_id]
            review_dict['user'] = user_obj.to_dict(safe=True) 

        place_id = review_dict.pop('place_id', None)
        if place_id and places_map and place_id in places_map:
            place_obj = places_map[place_id]
            review_dict['place'] = place_obj.to_dict(safe=True)

        return review_dict