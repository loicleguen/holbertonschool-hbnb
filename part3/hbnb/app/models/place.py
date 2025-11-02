#!/usr/bin/python3
"""Defines the Place model with SQLAlchemy"""

from app import db
from app.models.BaseModel import BaseModel
from sqlalchemy.orm import validates
from decimal import Decimal


# Association table for Many-to-Many relationship between Place and Amenity
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id', ondelete='CASCADE'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id', ondelete='CASCADE'), primary_key=True)
)


class Place(BaseModel):
    """Place model mapped to database table"""
    
    __tablename__ = 'places'
    
    # SQLAlchemy columns
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    # Foreign key (One-to-Many relationship with User)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Relationships
    owner = db.relationship('User', back_populates='places')
    reviews = db.relationship('Review', backref='place', lazy=True, cascade='all, delete-orphan')
    amenities = db.relationship('Amenity', secondary=place_amenity, lazy='subquery', back_populates='places')

    def __init__(self, title=None, description=None, price=None, latitude=None, 
                 longitude=None, owner_id=None, amenities=None, **kwargs):
        """Initialize Place instance"""
        super().__init__(**kwargs)
        
        if title:
            self.title = title
        if description:
            self.description = description
        if price is not None:
            self.price = price
        if latitude is not None:
            self.latitude = latitude
        if longitude is not None:
            self.longitude = longitude
        if owner_id:
            self.owner_id = owner_id
        if amenities:
            self.amenities = amenities if isinstance(amenities, list) else []

    @validates('title')
    def validate_title(self, key, value):
        """Validate title"""
        if not value or not isinstance(value, str) or not value.strip():
            raise ValueError("title must be a non-empty string")
        if len(value) > 255:
            raise ValueError("title must be less than 255 characters")
        return value.strip()

    @validates('price')
    def validate_price(self, key, value):
        """Validate price"""
        if value is None:
            raise ValueError("Price is required")
        
        # Convert to Decimal for precision
        try:
            decimal_value = Decimal(str(value))
        except:
            raise TypeError("Price must be a number")
        
        if decimal_value < 0:
            raise ValueError("Price must be non-negative")
        
        return decimal_value

    @validates('latitude')
    def validate_latitude(self, key, value):
        """Validate latitude"""
        if value is None or not isinstance(value, (int, float)):
            raise TypeError("Latitude must be a number")
        if value < -90 or value > 90:
            raise ValueError("Latitude must be between -90 and 90")
        return float(value)

    @validates('longitude')
    def validate_longitude(self, key, value):
        """Validate longitude"""
        if value is None or not isinstance(value, (int, float)):
            raise TypeError("Longitude must be a number")
        if value < -180 or value > 180:
            raise ValueError("Longitude must be between -180 and 180")
        return float(value)

    def add_amenity(self, amenity):
        """Add an amenity to the place (SQLAlchemy way)"""
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def to_dict(self, owners_map=None, amenities_map=None, reviews_map=None, **kwargs):
        """
        Returns a dictionary representation of the Place
        """
        place_dict = super().to_dict(**kwargs)
        
        # Convert Decimal to float for JSON serialization
        if 'price' in place_dict and isinstance(place_dict['price'], Decimal):
            place_dict['price'] = float(place_dict['price'])

        # ----- OWNER -----
        owner_id = place_dict.get('owner_id')
        if owner_id and owners_map and owner_id in owners_map:
            owner_obj = owners_map[owner_id]
            place_dict['owner'] = owner_obj.to_dict()
            place_dict.pop('owner_id', None)
        else:
            place_dict['owner'] = {
                'id': owner_id,
                'first_name': None,
                'last_name': None,
                'email': None
            }
            place_dict.pop('owner_id', None)

        # ----- AMENITIES -----
        # SQLAlchemy amenities is already a list of Amenity objects
        amenity_objs = self.amenities if hasattr(self, 'amenities') else []
        place_dict['amenities'] = []
        
        for amenity in amenity_objs:
            if hasattr(amenity, 'to_dict'):
                place_dict['amenities'].append(amenity.to_dict())
            elif hasattr(amenity, 'id'):
                place_dict['amenities'].append({'id': amenity.id, 'name': getattr(amenity, 'name', None)})

        # ----- REVIEWS -----
        place_dict['reviews'] = []
        if reviews_map:
            for r in reviews_map:
                if hasattr(r, 'to_dict'):
                    place_dict['reviews'].append(r.to_dict())
                else:
                    place_dict['reviews'].append({
                        'id': getattr(r, 'id', None),
                        'text': getattr(r, 'text', None),
                        'rating': getattr(r, 'rating', None)
                    })

        return place_dict

    def __repr__(self):
        """String representation of Place"""
        return f"<Place {self.title}>"