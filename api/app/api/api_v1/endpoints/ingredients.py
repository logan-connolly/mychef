from typing import Any, Dict, List, Optional

from asyncpg.exceptions import UniqueViolationError
from fastapi import APIRouter, HTTPException
from orm.exceptions import NoMatch
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from app.models import Ingredient
from app.schemas import IngredientDB, IngredientCreate, IngredientUpdate

router = APIRouter()


@router.get("/", response_model=List[IngredientDB], status_code=HTTP_200_OK)
async def get_ingredients(query: Optional[str] = None):
    ingredients = await (
        Ingredient.objects.filter(ingredient__contains=query).all()
        if query
        else Ingredient.objects.all()
    )
    if not ingredients:
        raise HTTPException(HTTP_404_NOT_FOUND, "No ingredients found")
    return ingredients


@router.post("/", response_model=IngredientDB, status_code=HTTP_201_CREATED)
async def add_ingredient(payload: IngredientCreate):
    try:
        return await Ingredient.objects.create(ingredient=payload.ingredient)
    except UniqueViolationError as err:
        raise HTTPException(HTTP_400_BAD_REQUEST, "Ingredient exists") from err


@router.get("/{ingred_id}/", response_model=IngredientDB, status_code=HTTP_200_OK)
async def get_ingredient(ingred_id: int):
    try:
        return await Ingredient.objects.get(id=ingred_id)
    except NoMatch as err:
        raise HTTPException(HTTP_404_NOT_FOUND, "Ingredient not found") from err


@router.put("/{ingred_id}/", response_model=IngredientDB, status_code=HTTP_200_OK)
async def update_ingredient(ingred_id: int, payload: IngredientUpdate):
    ingredient = await get_ingredient(ingred_id)
    updates: Dict[str, Any] = {k: v for k, v in payload.dict().items() if v is not None}
    await ingredient.update(**updates)
    return await get_ingredient(ingred_id)


@router.delete("/{ingred_id}/", response_model=IngredientDB, status_code=HTTP_200_OK)
async def remove_ingredient(ingred_id: int):
    ingredient = await get_ingredient(ingred_id)
    await ingredient.delete()
    return ingredient
