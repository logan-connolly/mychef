from pydantic import BaseModel, AnyUrl
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.sql import func

from app.models.base import Base


class RecipeSchema(BaseModel):
    name: str
    url: AnyUrl
    image: AnyUrl


class RecipeDB(RecipeSchema):
    id: int
    sid: int


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    url = Column(String(255))
    image = Column(String(255))
    sid = Column(Integer, ForeignKey("sources.id", ondelete="CASCADE"))
    ts = Column(DateTime, default=func.now(), nullable=False)

    def __repr__(self):
        return f"Recipe({self.id}, '{self.name}')"
