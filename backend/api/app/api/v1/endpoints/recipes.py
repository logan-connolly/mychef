from typing import Any, Dict

import httpx
from asyncpg.exceptions import UniqueViolationError
from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page, paginate
from orm.exceptions import NoMatch
from starlette.requests import Request
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from app.core.config import settings
from app.models import Ingredient, Recipe
from app.schemas import RecipeAdd, RecipeCreate, RecipeDB, RecipeUpdate, SourceDB

from .sources import get_source

router = APIRouter()


@router.get("/", response_model=Page[RecipeDB], status_code=HTTP_200_OK)
async def get_recipes(sid: int):
    recipes = await Recipe.objects.filter(source=sid).all()
    if not recipes:
        raise HTTPException(HTTP_404_NOT_FOUND, "No recipes found")
    return paginate(recipes)


@router.post("/", response_model=RecipeDB, status_code=HTTP_201_CREATED)
async def add_recipe(request: Request, sid: int, payload: RecipeAdd):
    cleaned_payload = await clean_payload(request, payload)
    source = await get_source(source_id=sid)
    return await update_recipe_data(source, cleaned_payload)


@router.get("/{recipe_id}/", response_model=RecipeDB, status_code=HTTP_200_OK)
async def get_recipe(sid: int, recipe_id: int):
    try:
        return await Recipe.objects.get(id=recipe_id, source=sid)
    except NoMatch as err:
        raise HTTPException(HTTP_404_NOT_FOUND, "Recipe not found") from err


@router.put("/{recipe_id}/", response_model=RecipeDB, status_code=HTTP_200_OK)
async def update_recipe(sid: int, recipe_id: int, payload: RecipeUpdate):
    recipe = await get_recipe(sid=sid, recipe_id=recipe_id)
    updates: Dict[str, Any] = {k: v for k, v in payload.dict().items() if v is not None}
    await recipe.update(**updates)
    return await get_recipe(sid=sid, recipe_id=recipe_id)


@router.delete("/{recipe_id}/", response_model=RecipeDB, status_code=HTTP_200_OK)
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
        raise HTTPException(HTTP_404_NOT_FOUND, "API model missing") from err


async def update_recipe_data(source: SourceDB, payload: RecipeCreate) -> RecipeDB:
    async def add_recipe():
        try:
            return await Recipe.objects.create(source=source, **payload.dict())
        except UniqueViolationError as err:
            raise HTTPException(HTTP_400_BAD_REQUEST, "Recipe exists") from err

    async def update_ingredients(recipe):
        for ingredient in recipe.ingredients["items"]:
            try:
                await Ingredient.objects.create(ingredient=ingredient)
            except UniqueViolationError:
                pass

    async def update_meili_recipe_index(recipe_id: int) -> None:
        data = {**payload.dict(), "id": recipe_id}
        async with httpx.AsyncClient() as client:
            await client.post(f"{settings.search_url}", json=[data])

    recipe = await add_recipe()
    await update_ingredients(recipe)
    await update_meili_recipe_index(recipe.id)
    return recipe
