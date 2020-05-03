from typing import Tuple

from databases import Database
from sqlalchemy import create_engine, MetaData

from .config import settings


def init_db() -> Tuple[Database, MetaData]:
    uri = settings.test_db_url if settings.testing else settings.db_url
    engine = create_engine(uri)
    metadata = MetaData()
    metadata.create_all(engine)
    return Database(uri), metadata


database, metadata = init_db()
