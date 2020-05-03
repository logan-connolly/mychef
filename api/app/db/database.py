from databases import Database
from sqlalchemy import create_engine, MetaData

from app.core.config import settings


metadata = MetaData()
engine = create_engine(settings.URI)
metadata.create_all(engine)
database = Database(settings.URI)
