#!/usr/bin/python3
"""DBStorage engine"""
from os import getenv
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """Database storage class"""
    __engine = None
    __session = None

    def __init__(self):
        """Create engine and link to MySQL database"""
        # URL encode the password to handle special characters
        encoded_pwd = quote_plus(getenv('HBNB_MYSQL_PWD', ''))
        
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                getenv('HBNB_MYSQL_USER'),
                encoded_pwd,  # Use the encoded password
                getenv('HBNB_MYSQL_HOST'),
                getenv('HBNB_MYSQL_DB')
            ),
            pool_pre_ping=True
        )

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects of a given class"""
        classes = [User, State, City, Amenity, Place, Review]
        objects = {}
        
        if cls:
            if cls in classes:
                results = self.__session.query(cls).all()
                for obj in results:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    objects[key] = obj
        else:
            for cls in classes:
                results = self.__session.query(cls).all()
                for obj in results:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    objects[key] = obj
        return objects

    def new(self, obj):
        """Add object to current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete object from current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables and initialize session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the current SQLAlchemy session"""
        self.__session.remove()