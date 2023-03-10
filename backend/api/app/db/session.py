from typing import AsyncGenerator

import meilisearch_python_async
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

engine = create_async_engine(settings.async_uri)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Async session to inject into API endpoints"""
    async with async_session() as session:
        yield session
        await session.commit()


async def get_mc() -> AsyncGenerator[meilisearch_python_async.Client, None]:
    """Get meiliseach client to interact with server."""
    async with meilisearch_python_async.Client(url=settings.meili_url) as client:
        yield client
