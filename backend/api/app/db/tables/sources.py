from sqlalchemy.sql import func
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import DateTime, Integer, String

from app.db.base import Base


class Source(Base):
    """Source information for recipe provider"""

    __tablename__ = "sources"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, max_length=255)
    url = Column(String, nullable=False, max_length=255)
    ts = Column(DateTime, default=func.now())
