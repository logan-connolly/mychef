from httpx import AsyncClient
from starlette import status

from app.core.config import settings


async def test_source_create(async_client: AsyncClient):
    """Test that source can be created"""
    url = f"{settings.api_version}/sources/"
    payload = {"name": "The Full Helping", "url": "https://fullhelping.com"}

    response = await async_client.post(url, json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "id": response.json()["id"],
        "name": payload["name"],
        "url": payload["url"],
    }
