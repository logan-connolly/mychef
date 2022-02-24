from httpx import AsyncClient
from starlette import status

from app.core.config import settings


async def test_ingredient_create(async_client: AsyncClient):
    """Test that ingredient can be created"""
    url = f"{settings.api_version}/ingredients/"
    payload = {"ingredient": "tomato"}

    response = await async_client.post(url, json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "id": response.json()["id"],
        "ingredient": payload["ingredient"],
    }
