from databases import Database
from sqlalchemy import MetaData

from app.core.config import settings

metadata = MetaData()
database = Database(settings.URI)
