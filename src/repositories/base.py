from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from databases import Database
from config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

database = Database(SQLALCHEMY_DATABASE_URL)
metadata = MetaData()
Base = declarative_base(metadata=metadata)
