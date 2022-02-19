from sqlalchemy.sql import func
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import JSON, DateTime, Integer, String

from app.db.base import Base


class Recipe(Base):
    """Recipe orm mapping to database"""

    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey("sources.id"))
    name = Column(String, nullable=False, max_length=255)
    url = Column(String, nullable=False, unique=True, max_length=255)
    image = Column(String, nullable=False, max_length=255)
    ingredients = Column(JSON, nullable=False)
    ts = Column(DateTime, default=func.now())
