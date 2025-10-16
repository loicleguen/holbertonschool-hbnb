from .BaseModel import BaseModel



class Review(BaseModel):
    def __init__(self, place_id=None, user_id=None, text=None, rating=None, *args, **kwargs):
        # BaseModel handles id, created_at, updated_at, and deserializes kwargs
        super().__init__(*args, **kwargs) 
        
        # Ensure attributes are set, prioritizing loaded values from BaseModel
        self.place_id = self.__dict__.get('place_id', place_id) 
        self.user_id = self.__dict__.get('user_id', user_id) 
        self.text = self.__dict__.get('text', text)
        self.rating = self.__dict__.get('rating', rating)


    def validate(self):
        if not hasattr(self, 'text') or not isinstance(self.text, str) or len(self.text) < 1:
            raise ValueError("text must be a non-empty string")
            
        if not hasattr(self, 'rating') or not isinstance(self.rating, int):
            raise TypeError("rating must be an integer")
        if not 1 <= self.rating <= 5:
            raise ValueError("rating must be between 1 and 5 ")
            
        # NOTE: Validation here should check for ID strings, not objects (Place, User)
        if not hasattr(self, 'place_id') or not isinstance(self.place_id, str) or not self.place_id:
            raise ValueError("place_id must be a non-empty string ID")
            
        if not hasattr(self, 'user_id') or not isinstance(self.user_id, str) or not self.user_id:
            raise TypeError("user_id must be a non-empty string ID")
            
        return True

    # app/models/review.py (Dans la classe Review)

    # Assurez-vous que cette méthode est celle qui est appelée par Flask-RESTx
    def to_dict(self, users_map=None, places_map=None, **kwargs):
        """
        Returns a dictionary representation of the Review, 
        including nested 'user' and 'place' objects if maps are provided.
        """
        # 1. Obtenir le dictionnaire de base de BaseModel (contient user_id et place_id)
        # Assurez-vous que super().to_dict() accepte **kwargs pour éviter l'erreur initiale.
        review_dict = super().to_dict(**kwargs) 
        
        # 2. Gestion des objets liés (User)
        user_id = review_dict.pop('user_id', None) # Retire l'ID pour le remplacer par l'objet
        if user_id and users_map and user_id in users_map:
            user_obj = users_map[user_id]
            # Le champ de sortie doit être 'user' (comme défini dans review_response_model)
            # On utilise to_dict du User pour ne pas inclure le mot de passe, etc.
            review_dict['user'] = user_obj.to_dict(safe=True) 
        else:
            # Fallback (ce cas ne devrait pas arriver si la Facade est bien codée)
            # Mais si on ne trouve pas l'objet, on ne renvoie rien pour 'user'
            # OU on réinsère l'ID si le modèle de réponse le permet (votre modèle n'inclut que 'user' et 'place')
            pass # Laissez simplement le champ 'user' manquant, Flask-RESTx le gérera comme null.

        
        # 3. Gestion des objets liés (Place)
        place_id = review_dict.pop('place_id', None) # Retire l'ID pour le remplacer par l'objet
        if place_id and places_map and place_id in places_map:
            place_obj = places_map[place_id]
            # Le champ de sortie doit être 'place' (comme défini dans review_response_model)
            review_dict['place'] = place_obj.to_dict(safe=True) 
        else:
            # Fallback
            pass 
            
        return review_dict
