from typing import List, Optional

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
from app.services.models import IngredientExtractor
from .sources import get_source


router = APIRouter()


@router.get("/", response_model=List[schemas.RecipeDB], status_code=HTTP_200_OK)
async def get_recipes(sid: int, limit: Optional[int] = None):
    recipes = await models.Recipe.objects.filter(source=sid).all()
    if not recipes:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No recipes found")
    if limit:
        return recipes[:limit]
    return recipes


@router.post("/", response_model=schemas.RecipeDB, status_code=HTTP_201_CREATED)
async def add_recipe(request: Request, sid: int, payload: schemas.RecipeCreate):
    try:
        source = await get_source(id=sid)
        model: IngredientExtractor = request.app.state.model
        ingredients = model.extract(payload.ingredients)
        for ingredient in ingredients:
            try:
                await models.Ingredient.objects.create(ingredient=ingredient)
            except UniqueViolationError:
                pass
        payload.ingredients = {"items": ingredients}
        return await models.Recipe.objects.create(source=source, **payload.dict())
    except UniqueViolationError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Recipe exists")


@router.get("/{id}/", response_model=schemas.RecipeDB, status_code=HTTP_200_OK)
async def get_recipe(sid: int, id: int):
    try:
        return await models.Recipe.objects.get(id=id, source=sid)
    except NoMatch:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Recipe not found")


@router.put("/{id}/", response_model=schemas.RecipeDB, status_code=HTTP_200_OK)
async def update_recipe(sid: int, id: int, payload: schemas.RecipeUpdate):
    recipe = await get_recipe(sid=sid, id=id)
    payload = {k: v for k, v in payload.dict().items() if v is not None}
    await recipe.update(**payload)
    return recipe


@router.delete("/{id}/", response_model=schemas.RecipeDB, status_code=HTTP_200_OK)
async def remove_recipe(sid: int, id: int):
    recipe = await get_recipe(sid=sid, id=id)
    await recipe.delete()
    return recipe
