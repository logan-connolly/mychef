import orm
from sqlalchemy.sql import func

from app.db.database import models


class Source(orm.Model):
    """Source orm mapping to database"""

    tablename = "sources"
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "name": orm.String(max_length=255),
        "url": orm.String(max_length=255, unique=True),
        "ts": orm.DateTime(default=func.now()),
    }
