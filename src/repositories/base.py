from databases import Database
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

from config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

database = Database(SQLALCHEMY_DATABASE_URL)
metadata = MetaData()

Base = declarative_base(metadata=metadata)
