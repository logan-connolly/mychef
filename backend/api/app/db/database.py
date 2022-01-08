from databases import Database
from orm import ModelRegistry
from sqlalchemy import MetaData

from app.core.config import settings

metadata = MetaData()
database = Database(url=settings.URI)
models = ModelRegistry(database=database)
