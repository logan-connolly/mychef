import os

from databases import Database
from sqlalchemy import create_engine

from .models.base import Base


DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
database = Database(DATABASE_URL)
