from typing import List, Optional

from asyncpg.exceptions import UniqueViolationError
from fastapi import APIRouter, HTTPException
from orm.exceptions import NoMatch
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from app import models, schemas


router = APIRouter()


@router.get("/", response_model=List[schemas.IngredientDB], status_code=HTTP_200_OK)
async def get_ingredients(query: Optional[str] = None):
    ingredients = await (
        models.Ingredient.objects.filter(ingredient__contains=query).all()
        if query
        else models.Ingredient.objects.all()
    )
    if not ingredients:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="No ingredients found")
    return ingredients


@router.post("/", response_model=schemas.IngredientDB, status_code=HTTP_201_CREATED)
async def add_ingredient(payload: schemas.IngredientCreate):
    try:
        return await models.Ingredient.objects.create(ingredient=payload.ingredient)
    except UniqueViolationError:
        raise HTTPException(HTTP_400_BAD_REQUEST, detail="Ingredient exists")


@router.get("/{id}/", response_model=schemas.IngredientDB, status_code=HTTP_200_OK)
async def get_ingredient(id: int):
    try:
        return await models.Ingredient.objects.get(id=id)
    except NoMatch:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="Ingredient not found")


@router.put("/{id}/", response_model=schemas.IngredientDB, status_code=HTTP_200_OK)
async def update_ingredient(id: int, payload: schemas.IngredientUpdate):
    ingredient = await get_ingredient(id)
    payload = {k: v for k, v in payload.dict().items() if v is not None}
    await ingredient.update(**payload)
    return ingredient


@router.delete("/{id}/", response_model=schemas.IngredientDB, status_code=HTTP_200_OK)
async def remove_ingredient(id: int):
    ingredient = await get_ingredient(id)
    await ingredient.delete()
    return ingredient
