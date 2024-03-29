from sqlalchemy.sql import func
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import DateTime, Integer, String

from app.db.tables.base import Base


class Source(Base):
    """Source information for recipe provider"""

    __tablename__ = "sources"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False, unique=True)
    ts = Column(DateTime, default=func.now())
