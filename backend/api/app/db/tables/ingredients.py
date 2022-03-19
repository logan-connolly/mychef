from sqlalchemy.sql import func
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import DateTime, Integer, String

from app.db.tables.base import Base


class Ingredient(Base):
    """Ingredient orm mapping to database"""

    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True)
    ingredient = Column(String(255), nullable=False, unique=True)
    ts = Column(DateTime, default=func.now())
