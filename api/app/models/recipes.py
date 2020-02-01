from pydantic import BaseModel, AnyUrl
from sqlalchemy import Column, DateTime, Integer, String, Table
from sqlalchemy.sql import func


class RecipeSchema(BaseModel):
    name: str
    url: AnyUrl
    image: AnyUrl


class RecipeDB(RecipeSchema):
    id: int


class Recipe:
    """Model for recipe metadata (name, url, image link)"""

    def __init__(self, metadata):
        self.metadata = metadata

    def create_table(self):
        return Table(
            "recipes",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(50)),
            Column("url", String(255)),
            Column("image", String(255)),
            Column("created_date", DateTime, default=func.now(), nullable=False),
        )
