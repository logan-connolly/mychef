import random
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
        raise HTTPException(HTTP_404_NOT_FOUND, detail="No recipes found")
    if limit:
        recipes = recipes[:limit]
    random.shuffle(recipes)
    return recipes


@router.post("/", response_model=schemas.RecipeDB, status_code=HTTP_201_CREATED)
async def add_recipe(request: Request, sid: int, payload: schemas.RecipeCreate):
    source = await get_source(id=sid)
    extracted_ingredients = await extract_ingredients(request, payload.ingredients)
    payload.ingredients = {"items": extracted_ingredients}
    try:
        return await models.Recipe.objects.create(source=source, **payload.dict())
    except UniqueViolationError:
        raise HTTPException(HTTP_400_BAD_REQUEST, detail="Recipe exists")


@router.get("/{id}/", response_model=schemas.RecipeDB, status_code=HTTP_200_OK)
async def get_recipe(sid: int, id: int):
    try:
        return await models.Recipe.objects.get(id=id, source=sid)
    except NoMatch:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="Recipe not found")


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


async def extract_ingredients(request: Request, ingredients: str) -> List[str]:
    model: IngredientExtractor = request.app.state.model
    if model is None:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="Ingredient extractor missing")
    extracted_ingredients = model.extract(ingredients)
    for ingredient in extracted_ingredients:
        try:
            await models.Ingredient.objects.create(ingredient=ingredient)
        except UniqueViolationError:
            pass
    return extracted_ingredients
