from pydantic import BaseModel, AnyUrl
from orm import Model, DateTime, Integer, String, ForeignKey
from sqlalchemy.sql import func

from ..db import database, metadata
from .sources import Source


class RecipeSchema(BaseModel):
    name: str
    url: AnyUrl
    image: AnyUrl


class RecipeDB(RecipeSchema):
    id: int


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
