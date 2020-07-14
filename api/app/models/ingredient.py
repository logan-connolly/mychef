from orm import Model, DateTime, Integer, String
from sqlalchemy.sql import func

from app.db.database import database, metadata


class Ingredient(Model):
    __tablename__ = "ingredients"
    __database__ = database
    __metadata__ = metadata

    id = Integer(primary_key=True)
    ingredient = String(max_length=255, unique=True)
    ts = DateTime(default=func.now())
