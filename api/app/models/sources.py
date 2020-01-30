from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Table
)
from sqlalchemy.sql import func


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
            Column("homepage", String(50)),
            Column("created_date", DateTime, default=func.now(), nullable=False),
       )

