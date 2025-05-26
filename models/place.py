#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

# Association table for many-to-many relationship
if getenv('HBNB_TYPE_STORAGE') == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
        Column('place_id', String(60), 
              ForeignKey('places.id'),
              primary_key=True,
              nullable=False),
        Column('amenity_id', String(60),
              ForeignKey('amenities.id'),
              primary_key=True,
              nullable=False)
    )

class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        
        # Relationships
        user = relationship("User", back_populates="places")
        city = relationship("City", back_populates="places")
        reviews = relationship("Review", back_populates="place",
                             cascade="all, delete-orphan")
        amenities = relationship(
            "Amenity",
            secondary="place_amenity",
            viewonly=False,
            back_populates="place_amenities"
        )
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

    def __init__(self, *args, **kwargs):
        """Initializes place"""
        super().__init__(*args, **kwargs)

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def reviews(self):
            """Getter for reviews in FileStorage mode"""
            from models import storage
            from models.review import Review
            return [review for review in storage.all(Review).values()
                    if review.place_id == self.id]

        @property
        def amenities(self):
            """Getter for amenities in FileStorage mode"""
            from models import storage
            from models.amenity import Amenity
            return [amenity for amenity in storage.all(Amenity).values()
                    if amenity.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            """Setter for amenities in FileStorage mode"""
            from models.amenity import Amenity
            if isinstance(obj, Amenity) and obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)