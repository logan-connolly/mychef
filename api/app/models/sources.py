from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, String, Table
from sqlalchemy.sql import func


class SourceSchema(BaseModel):
    name: str
    url: str


class SourceDB(SourceSchema):
    id: int


class Source:
    """Model for recipe source website"""

    def __init__(self, metadata):
        self.metadata = metadata

    def create_table(self):
        return Table(
            "sources",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(50)),
            Column("url", String(50)),
            Column("created_date", DateTime, default=func.now(), nullable=False),
        )
