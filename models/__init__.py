from os import getenv
import pymysql  # <--- Add this import
pymysql.install_as_MySQLdb()  # <--- Add this line to patch MySQLdb with pymysql

# Phase 1: Storage Configuration (No Model Imports)
storage_t = getenv('HBNB_TYPE_STORAGE')

# Phase 2: Storage Initialization
if storage_t == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

# Phase 3: Model Imports (Strict Dependency Order)
# 1. Base classes
from models.base_model import BaseModel, Base

# 2. Independent models
from models.user import User
from models.state import State

# 3. Dependent models
from models.city import City          # Depends on State
from models.amenity import Amenity

# 4. Highly dependent models
from models.place import Place       # Depends on User, City
from models.review import Review     # Depends on User, Place

# Phase 4: Final Initialization
storage.reload()

# Clean namespace
del getenv, storage_t, pymysql
