import orm
from sqlalchemy.sql import func

from app.db.database import models

from .source import Source


class Recipe(orm.Model):
    """Recipe orm mapping to database"""

    tablename = "recipes"
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "source": orm.ForeignKey(Source),
        "name": orm.String(max_length=255),
        "url": orm.String(max_length=255, unique=True),
        "image": orm.String(max_length=255),
        "ingredients": orm.JSON(),
        "ts": orm.DateTime(default=func.now()),
    }
