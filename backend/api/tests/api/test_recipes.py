import pytest
from httpx import AsyncClient
from starlette import status

from app.core.config import settings


@pytest.fixture
async def example_source_id(async_client) -> str:
    """Add example source to add a recipe to"""
    source_url = f"{settings.api_version}/sources/"
    source_payload = {"name": "The Full Helping", "url": "https://fullhelping.com"}
    response = await async_client.post(source_url, json=source_payload)
    return response.json()["id"]


async def test_recipe_create(async_client: AsyncClient, example_source_id: str):
    """Test that recipe can be created"""
    recipe_url = f"{settings.api_version}/recipes/"
    payload = {
        "name": "Fancy recipe",
        "source_id": example_source_id,
        "url": "https://fullhelping.com/fancy-recipe",
        "image": "https://fullhelping.com/fancy-recipe.png",
        "ingredients": "Add 1 tablespoon of onion powder",
    }

    response = await async_client.post(recipe_url, json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "id": response.json()["id"],
        "source_id": payload["source_id"],
        "name": payload["name"],
        "url": payload["url"],
        "image": payload["image"],
        "ingredients": {"items": ["onion powder"]},
    }
