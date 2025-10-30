from app import db
from app.models.BaseModel import BaseModel 

class Review(BaseModel):
    """
    Represents a review for a place, mapped to the 'reviews' table.
    Inherits id, created_at, and updated_at (UUID, timestamps) from BaseModel.
    """
    __tablename__ = 'reviews'

    # Core Attributes (as per task instructions)
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False) # Rating from 1 to 5
    
    # Note: user_id and place_id relationships will be added in later tasks.

    def __repr__(self):
        """Returns a string representation of the object."""
        return f"<Review {self.id} - Rating: {self.rating}>"
