from sqlalchemy.sql import func
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import JSON, DateTime, Integer, String

from app.db.tables.base import Base


class Recipe(Base):
    """Recipe orm mapping to database"""

    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey("sources.id"))
    name = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False, unique=True)
    image = Column(String(255), nullable=False)
    ingredients = Column(JSON, nullable=False)
    ts = Column(DateTime, default=func.now())
