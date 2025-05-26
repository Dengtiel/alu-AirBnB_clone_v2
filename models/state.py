#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship(
            "City",
            back_populates="state",  # Requires matching relationship in City
            cascade="all, delete-orphan",
            single_parent=True  # Additional safety for delete-orphan
        )
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            """getter for list of city instances related to the state"""
            from models import storage
            from models.city import City
            return [city for city in storage.all(City).values() 
                   if city.state_id == self.id]