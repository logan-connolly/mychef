from orm import Model, DateTime, Integer, String, ForeignKey
from sqlalchemy.sql import func

from app.db.database import database, metadata
from .source import Source


class Recipe(Model):
    __tablename__ = "recipes"
    __database__ = database
    __metadata__ = metadata

    id = Integer(primary_key=True)
    source = ForeignKey(Source)
    name = String(max_length=255)
    url = String(max_length=255, unique=True)
    image = String(max_length=255)
    ts = DateTime(default=func.now())
