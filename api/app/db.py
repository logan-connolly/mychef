import os

from databases import Database
from sqlalchemy import create_engine, MetaData

from .models.sources import Source
from .models.recipes import Recipe


DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Init Models
sources = Source(metadata).create_table()
recipes = Recipe(metadata).create_table()

database = Database(DATABASE_URL)
