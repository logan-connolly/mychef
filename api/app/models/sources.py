from pydantic import BaseModel, AnyUrl
from orm import Model, DateTime, Integer, String
from sqlalchemy.sql import func

from app.db import database, metadata


class SourceSchema(BaseModel):
    name: str
    url: AnyUrl


class SourceDB(SourceSchema):
    id: int
    url: str


class Source(Model):
    __tablename__ = "sources"
    __database__ = database
    __metadata__ = metadata

    id = Integer(primary_key=True)
    name = String(max_length=255)
    url = String(max_length=255)
    ts = DateTime(default=func.now())
