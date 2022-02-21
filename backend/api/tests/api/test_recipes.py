from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.config import settings
from app.db.repositories.recipes import RecipesRepository


async def test_recipe_create(async_client: AsyncClient, db_session: AsyncSession):
    """Test that recipe can be created"""
    recipes_repository = RecipesRepository(db_session)
    source_url = f"{settings.api_version}/sources/"
    recipe_url = f"{settings.api_version}/recipes/"
    source_payload = {
        "name": "The Full Helping",
        "url": "https://fullhelping.com",
    }
    payload = {
        "name": "Fancy recipe",
        "source_id": 1,
        "url": "https://fullhelping.com/fancy-recipe",
        "image": "https://fullhelping.com/fancy-recipe.png",
        "ingredients": "Add 1 tablespoon of onion powder",
    }

    response = await async_client.post(source_url, json=source_payload)
    response = await async_client.post(recipe_url, json=payload)
    recipe = await recipes_repository.get_by_id(response.json()["id"])

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "id": recipe.id,
        "source_id": payload["source_id"],
        "name": payload["name"],
        "url": payload["url"],
        "image": payload["image"],
        "ingredients": {"items": ["onion powder"]},
    }
