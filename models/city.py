#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'cities'
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        
        # Relationship with State
        state = relationship(
            "State",
            back_populates="cities"  # Must match State's back_populates
        )
        
        # Relationship with Place
        places = relationship(
            "Place",
            back_populates="city",
            cascade="all, delete-orphan",
            single_parent=True
        )
    else:
        state_id = ""
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def state(self):
            """Getter for the state associated with this city"""
            from models import storage
            from models.state import State
            return storage.get(State, self.state_id)