import orm
from sqlalchemy.sql import func

from app.db.database import database, metadata

from .source import Source


class Recipe(orm.Model):
    __tablename__ = "recipes"
    __database__ = database
    __metadata__ = metadata

    id = orm.Integer(primary_key=True)
    source = orm.ForeignKey(Source)
    name = orm.String(max_length=255)
    url = orm.String(max_length=255, unique=True)
    image = orm.String(max_length=255)
    ingredients = orm.JSON()
    ts = orm.DateTime(default=func.now())
