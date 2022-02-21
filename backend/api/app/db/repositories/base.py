import abc
from typing import Generic, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.exceptions import DoesNotExist
from app.db.base import Base
from app.schemas.base import BaseSchema

InSchema = TypeVar("InSchema", bound=BaseSchema)
Schema = TypeVar("Schema", bound=BaseSchema)
Table = TypeVar("Table", bound=Base)
Filter = tuple[str, str]


class BaseRepository(Generic[InSchema, Schema, Table], metaclass=abc.ABCMeta):
    """Define single point of entry for handling data in the database"""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @property
    @abc.abstractmethod
    def _table(self) -> Type[Table]:
        ...

    @property
    @abc.abstractmethod
    def _schema(self) -> Type[Schema]:
        ...

    async def create(self, in_schema: InSchema) -> Schema:
        """Create entry into DB after validating input schema"""
        entry = self._table(**in_schema.dict())
        self._session.add(entry)
        await self._session.commit()
        return self._schema.from_orm(entry)

    async def get_by_id(self, id: int) -> Schema:
        """Fetch ORM entry by id, raising exception if not found"""
        entry = await self._session.get(self._table, id)
        if not entry:
            raise DoesNotExist(f"{self._table.__name__}<id:{id}> does not exist")
        return self._schema.from_orm(entry)

    async def get_all(self) -> list[Schema]:
        """Fetch all entries from ORM"""
        results = await self._session.execute(select(self._table))
        return [result for result in results.scalars()]
