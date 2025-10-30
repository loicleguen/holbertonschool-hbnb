from app import db
from app.models.BaseModel import BaseModel 

class Amenity(BaseModel):
    """
    Represents an amenity, mapped to the 'amenities' table.
    Inherits id, created_at, and updated_at (UUID, timestamps) from BaseModel.
    """
    __tablename__ = 'amenities'

    # Core Attribute (as per task instructions)
    name = db.Column(db.String(80), nullable=False, unique=True)

    def __repr__(self):
        """Returns a string representation of the object."""
        return f"<Amenity {self.id} - {self.name}>"
