from typing import Type

from app.db.repositories.base import BaseRepository
from app.db.tables.sources import Source
from app.schemas.sources import InSourceSchema, SourceSchema


class SourcesRepository(BaseRepository[InSourceSchema, SourceSchema, Source]):
    @property
    def _schema(self) -> Type[SourceSchema]:
        return SourceSchema

    @property
    def _table(self) -> Type[Source]:
        return Source
