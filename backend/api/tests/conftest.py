import asyncio
from typing import AsyncGenerator, Callable, Generator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.db.session import async_session, engine
from app.db.tables.base import Base


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create test database session that will then be reverted after test run"""
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
        async with async_session(bind=connection) as session:
            yield session
            await session.flush()
            await session.rollback()


@pytest.fixture
def override_get_db(db_session: AsyncSession) -> Callable:
    """Make database session an async callable to pass to get_db dependency"""

    async def _override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    return _override_get_db


@pytest.fixture()
async def async_client(override_get_db: Callable) -> AsyncGenerator:
    """Create test client to be used to test api endpoints"""
    from app.db.session import get_db
    from app.main import app

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client
