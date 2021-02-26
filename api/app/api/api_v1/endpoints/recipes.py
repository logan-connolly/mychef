import random
from typing import Any, Dict, List, Optional

import httpx
from asyncpg.exceptions import UniqueViolationError
from fastapi import APIRouter, HTTPException
from orm.exceptions import NoMatch
from starlette.requests import Request
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from app.models import Recipe, Ingredient
from app.schemas import RecipeDB, RecipeAdd, RecipeUpdate, RecipeCreate, SourceDB
from app.core.config import settings
from .sources import get_source

router = APIRouter()


@router.get("/", response_model=List[RecipeDB], status_code=HTTP_200_OK)
async def get_recipes(sid: int, limit: Optional[int] = None):
    recipes = await Recipe.objects.filter(source=sid).all()
    if not recipes:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="No recipes found")
    n_recipes = len(recipes)
    n_samples = limit if limit and limit < n_recipes else n_recipes
    return random.sample(recipes, n_samples)


@router.post("/", response_model=RecipeDB, status_code=HTTP_201_CREATED)
async def add_recipe(request: Request, sid: int, payload: RecipeAdd):
    cleaned_payload = await clean_payload(request, payload)
    source = await get_source(id=sid)
    return await update_recipe_data(source, cleaned_payload)


@router.get("/{id}/", response_model=RecipeDB, status_code=HTTP_200_OK)
async def get_recipe(sid: int, recipe_id: int):
    try:
        return await Recipe.objects.get(id=recipe_id, source=sid)
    except NoMatch as err:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="Recipe not found") from err


@router.put("/{id}/", response_model=RecipeDB, status_code=HTTP_200_OK)
async def update_recipe(sid: int, recipe_id: int, payload: RecipeUpdate):
    recipe = await get_recipe(sid=sid, recipe_id=recipe_id)
    updates: Dict[str, Any] = {k: v for k, v in payload.dict().items() if v is not None}
    return await recipe.update(**updates)


@router.delete("/{id}/", response_model=RecipeDB, status_code=HTTP_200_OK)
async def remove_recipe(sid: int, recipe_id: int):
    recipe = await get_recipe(sid=sid, recipe_id=recipe_id)
    await recipe.delete()
    return recipe


async def clean_payload(req: Request, data: RecipeAdd) -> RecipeCreate:
    try:
        items = {"items": req.app.state.ingredient_model.extract(data.ingredients)}
        return RecipeCreate(
            name=data.name, url=data.url, image=data.image, ingredients=items
        )
    except AttributeError as err:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="API model missing") from err


async def update_recipe_data(source: SourceDB, payload: RecipeCreate) -> RecipeDB:
    async def add_recipe():
        try:
            return await Recipe.objects.create(source=source, **payload.dict())
        except UniqueViolationError as err:
            raise HTTPException(HTTP_400_BAD_REQUEST, detail="Recipe exists") from err

    async def update_ingredients(recipe):
        for ingredient in recipe.ingredients["items"]:
            try:
                await Ingredient.objects.create(ingredient=ingredient)
            except UniqueViolationError:
                pass

    async def update_meili_recipe_index(recipe_id: int) -> None:
        data = {**payload.dict(), "id": recipe_id}
        async with httpx.AsyncClient() as client:
            return await client.post(f"{settings.SEARCH_URL}", json=[data])

    recipe = await add_recipe()
    await update_ingredients(recipe)
    await update_meili_recipe_index(recipe.id)
    return recipe
