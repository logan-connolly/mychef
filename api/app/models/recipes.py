from pydantic import BaseModel, AnyUrl
from orm import Model, DateTime, Integer, String, ForeignKey
from sqlalchemy.sql import func

from app.db import database, metadata
from app.models.sources import Source


class RecipeSchema(BaseModel):
    name: str
    url: AnyUrl
    image: AnyUrl


class RecipeDB(RecipeSchema):
    id: int
    sid: int


class Recipe(Model):
    __tablename__ = "recipes"
    __database__ = database
    __metadata__ = metadata

    id = Integer(primary_key=True)
    name = String(255)
    url = String(255)
    image = String(255)
    sid = ForeignKey(Source)
    ts = DateTime(default=func.now())
