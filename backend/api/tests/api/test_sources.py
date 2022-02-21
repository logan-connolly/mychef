from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.config import settings
from app.db.repositories.sources import SourcesRepository


async def test_source_create(async_client: AsyncClient, db_session: AsyncSession):
    """Test that source can be created"""
    sources_repository = SourcesRepository(db_session)
    url = f"{settings.api_version}/sources/"
    payload = {"name": "The Full Helping", "url": "https://fullhelping.com"}

    response = await async_client.post(url, json=payload)
    source = await sources_repository.get_by_id(response.json()["id"])

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "id": source.id,
        "name": payload["name"],
        "url": payload["url"],
    }
