import random
from typing import Any, Dict, List, Optional

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
    n_recipes = len(recipes)
    n_samples = limit if limit and limit < n_recipes else n_recipes
    return random.sample(recipes, n_samples)


@router.post("/", response_model=schemas.RecipeDB, status_code=HTTP_201_CREATED)
async def add_recipe(request: Request, sid: int, payload: schemas.RecipeAdd):
    ingredients = await extract(request, payload.ingredients)
    name, url, image = payload.name, payload.url, payload.image
    newload: schemas.RecipeCreate = schemas.RecipeCreate(
        name=name, url=url, image=image, ingredients=ingredients
    )
    source = await get_source(id=sid)
    try:
        return await models.Recipe.objects.create(source=source, **newload.dict())
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
    updates: Dict[str, Any] = {k: v for k, v in payload.dict().items() if v is not None}
    await recipe.update(**updates)
    return recipe


@router.delete("/{id}/", response_model=schemas.RecipeDB, status_code=HTTP_200_OK)
async def remove_recipe(sid: int, id: int):
    recipe = await get_recipe(sid=sid, id=id)
    await recipe.delete()
    return recipe


async def extract(request: Request, ingredients: str) -> Dict[str, List[str]]:
    model: IngredientExtractor = request.app.state.model
    if model is None:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="Ingredient extractor missing")
    extracted_ingredients = model.extract(ingredients)
    for ingredient in extracted_ingredients:
        try:
            await models.Ingredient.objects.create(ingredient=ingredient)
        except UniqueViolationError:
            pass
    return {"items": extracted_ingredients}
