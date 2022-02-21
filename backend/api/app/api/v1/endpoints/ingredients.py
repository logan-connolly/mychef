from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from app.core.exceptions import DoesNotExist
from app.db.repositories.ingredients import IngredientsRepository
from app.db.session import get_db
from app.schemas.ingredients import IngredientSchema, InIngredientSchema

router = APIRouter()


@router.post("/", response_model=IngredientSchema, status_code=HTTP_201_CREATED)
async def add_ingredient(
    payload: InIngredientSchema, db: AsyncSession = Depends(get_db)
):
    repo = IngredientsRepository(db)
    try:
        return await repo.create(payload)
    except IntegrityError:
        raise HTTPException(HTTP_400_BAD_REQUEST, "Ingredient exists")


@router.get("/{ingred_id}/", response_model=IngredientSchema, status_code=HTTP_200_OK)
async def get_ingredient(ingred_id: int, db: AsyncSession = Depends(get_db)):
    repo = IngredientsRepository(db)
    try:
        return await repo.get_by_id(ingred_id)
    except DoesNotExist:
        raise HTTPException(HTTP_404_NOT_FOUND, "Ingredient not found")


@router.get("/", response_model=list[IngredientSchema], status_code=HTTP_200_OK)
async def get_ingredients(db: AsyncSession = Depends(get_db)):
    repo = IngredientsRepository(db)
    return await repo.get_all()
