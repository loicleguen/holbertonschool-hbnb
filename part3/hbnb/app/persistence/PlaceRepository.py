from app import db
from app.models.BaseModel import BaseModel 

class Place(BaseModel):
    """
    Represents a place (rental listing), mapped to the 'places' table.
    Inherits id, created_at, and updated_at (UUID, timestamps) from BaseModel.
    """
    __tablename__ = 'places'

    # Core Attributes (as per task instructions)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True) 
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    # Note: owner_id, city_id, and amenity relationships will be added in later tasks.

    def __repr__(self):
        """Returns a string representation of the object."""
        return f"<Place {self.id} - {self.title}>"
