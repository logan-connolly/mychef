from typing import AsyncGenerator

import meilisearch
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

engine = create_async_engine(settings.async_uri)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Async session to inject into API endpoints"""
    async with async_session() as session:
        yield session
        await session.commit()


def get_mc() -> meilisearch.Client:
    """Get meiliseach client to interact with server."""
    return meilisearch.Client(url=settings.meili_url)
