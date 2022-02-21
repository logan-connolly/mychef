from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.config import settings
from app.db.repositories.ingredients import IngredientsRepository


async def test_ingredient_create(async_client: AsyncClient, db_session: AsyncSession):
    """Test that ingredient can be created"""
    ingredients_repository = IngredientsRepository(db_session)
    url = f"{settings.api_version}/ingredients/"
    payload = {"ingredient": "tomato"}

    response = await async_client.post(url, json=payload)
    ingredient = await ingredients_repository.get_by_id(response.json()["id"])

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"id": ingredient.id, "ingredient": payload["ingredient"]}
