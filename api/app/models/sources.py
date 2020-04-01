from pydantic import BaseModel, AnyUrl
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.models.base import Base


class SourceSchema(BaseModel):
    name: str
    url: AnyUrl


class SourceDB(SourceSchema):
    id: int
    url: str


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    url = Column(String(255))
    ts = Column(DateTime, default=func.now(), nullable=False)

    def __repr__(self):
        return f"Source({self.id}, '{self.name}')"
