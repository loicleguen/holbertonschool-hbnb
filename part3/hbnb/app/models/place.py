#!/usr/bin/python3
"""Defines the Place model with SQLAlchemy"""

from app import db
from app.models.BaseModel import BaseModel
from sqlalchemy.orm import validates
from decimal import Decimal


# Association table for One-to-Many relationship between Place and Amenity
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

    def to_dict(self, **kwargs):
        """
        Returns a dictionary representation of the Place
        
        All relationships (owner, amenities, reviews) are loaded via SQLAlchemy
        """
        place_dict = super().to_dict(**kwargs)
        
        # Convert Decimal to float for JSON serialization
        if 'price' in place_dict and isinstance(place_dict['price'], Decimal):
            place_dict['price'] = float(place_dict['price'])

        # ----- OWNER ----- (SQLAlchemy relationship)
        if hasattr(self, 'owner') and self.owner:
            place_dict['owner'] = {
                'id': self.owner.id,
                'first_name': self.owner.first_name,
                'last_name': self.owner.last_name,
                'email': self.owner.email
            }
        else:
            # Fallback si owner n'est pas chargé
            place_dict['owner'] = {
                'id': place_dict.get('owner_id'),
                'first_name': None,
                'last_name': None,
                'email': None
            }
        place_dict.pop('owner_id', None)

        # ----- AMENITIES ----- (SQLAlchemy relationship)
        place_dict['amenities'] = []
        if hasattr(self, 'amenities') and self.amenities:
            for amenity in self.amenities:
                place_dict['amenities'].append({
                    'id': amenity.id,
                    'name': amenity.name
                })

        # ----- REVIEWS ----- (SQLAlchemy relationship)
        place_dict['reviews'] = []
        if hasattr(self, 'reviews') and self.reviews:
            for review in self.reviews:
                place_dict['reviews'].append({
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'user_id': review.user_id
                })

        return place_dict

    def __repr__(self):
        """String representation of Place"""
        return f"<Place {self.title}>"