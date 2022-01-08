from orm import DateTime, Integer, Model, String
from sqlalchemy.sql import func

from app.db.database import models


class Ingredient(Model):
    """Ingredient orm mapping to database"""

    tablename = "ingredients"
    registry = models
    fields = {
        "id": Integer(primary_key=True),
        "ingredient": String(max_length=255, unique=True),
        "ts": DateTime(default=func.now()),
    }
