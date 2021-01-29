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

from app import models, schemas
from app.core.config import settings
from .sources import get_source


router = APIRouter()


@router.get("/", response_model=List[schemas.RecipeDB], status_code=HTTP_200_OK)
async def get_recipes(sid: int, limit: Optional[int] = None):
    recipes = await models.Recipe.objects.filter(source=sid).all()
    if not recipes:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="No recipes found")
    n_recipes = len(recipes)
    n_samples = limit if limit and limit < n_recipes else n_recipes
    return random.sample(recipes, n_samples)


@router.post("/", response_model=schemas.RecipeDB, status_code=HTTP_201_CREATED)
async def add_recipe(request: Request, sid: int, payload: schemas.RecipeAdd):
    cleaned_payload = await clean_payload(request, payload)
    source = await get_source(id=sid)
    return await update_recipe_data(source, cleaned_payload)


@router.get("/{id}/", response_model=schemas.RecipeDB, status_code=HTTP_200_OK)
async def get_recipe(sid: int, id: int):
    try:
        return await models.Recipe.objects.get(id=id, source=sid)
    except NoMatch:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="Recipe not found")


@router.put("/{id}/", response_model=schemas.RecipeDB, status_code=HTTP_200_OK)
async def update_recipe(sid: int, id: int, payload: schemas.RecipeUpdate):
    recipe = await get_recipe(sid=sid, id=id)
    updates: Dict[str, Any] = {k: v for k, v in payload.dict().items() if v is not None}
    await recipe.update(**updates)
    return recipe


@router.delete("/{id}/", response_model=schemas.RecipeDB, status_code=HTTP_200_OK)
async def remove_recipe(sid: int, id: int):
    recipe = await get_recipe(sid=sid, id=id)
    await recipe.delete()
    return recipe


async def clean_payload(req: Request, data: schemas.RecipeAdd) -> schemas.RecipeCreate:
    try:
        return schemas.RecipeCreate(
            name=data.name,
            url=data.url,
            image=data.image,
            ingredients={"items": req.app.state.model.extract(data.ingredients)},
        )
    except AttributeError as err:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="API model missing") from err


async def update_recipe_data(
    source: schemas.SourceDB, payload: schemas.RecipeCreate
) -> schemas.RecipeDB:
    async def update_recipe_in_db():
        try:
            recipe = await models.Recipe.objects.create(source=source, **payload.dict())
            for ingredient in recipe.ingredients["items"]:
                try:
                    await models.Ingredient.objects.create(ingredient=ingredient)
                except UniqueViolationError:
                    pass
            return recipe
        except UniqueViolationError as err:
            raise HTTPException(HTTP_400_BAD_REQUEST, detail="Recipe exists") from err

    async def update_meili_recipe_index(recipe: schemas.RecipeDB) -> None:
        endpoint = "/indexes/recipes/documents"
        data = dict(
            id=recipe.id, name=recipe.name, ingredients=recipe.ingredients["items"]
        )
        async with httpx.AsyncClient() as client:
            await client.post(f"{settings.SEARCH_URL}{endpoint}", json=[data])

    resp = await update_recipe_in_db()
    await update_meili_recipe_index(resp)
    return resp
