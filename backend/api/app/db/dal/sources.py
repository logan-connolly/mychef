from typing import Type

from app.db.dal.base import BaseDAL
from app.db.tables.sources import Source
from app.schemas.sources import InSourceSchema, SourceSchema


class SourcesDAL(BaseDAL[InSourceSchema, SourceSchema, Source]):
    @property
    def _schema(self) -> Type[SourceSchema]:
        return SourceSchema

    @property
    def _table(self) -> Type[Source]:
        return Source
