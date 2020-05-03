from orm import Model, DateTime, Integer, String
from sqlalchemy.sql import func

from ..db import database, metadata


class Source(Model):
    __tablename__ = "sources"
    __database__ = database
    __metadata__ = metadata

    id = Integer(primary_key=True)
    name = String(max_length=255)
    url = String(max_length=255, unique=True)
    ts = DateTime(default=func.now())
