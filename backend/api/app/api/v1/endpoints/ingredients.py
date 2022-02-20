from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from app.db.repositories.ingredients import IngredientsRepository
from app.db.session import get_db
from app.schemas.ingredients import IngredientSchema, InIngredientSchema

router = APIRouter()


@router.post("/", response_model=IngredientSchema, status_code=HTTP_201_CREATED)
async def add_ingredient(
    payload: InIngredientSchema, db: AsyncSession = Depends(get_db)
):
    repo = IngredientsRepository(db)
    return await repo.create(payload)


@router.get("/{ingred_id}/", response_model=IngredientSchema, status_code=HTTP_200_OK)
async def get_ingredient(ingred_id: int, db: AsyncSession = Depends(get_db)):
    repo = IngredientsRepository(db)
    return await repo.get_by_id(ingred_id)


@router.get("/", response_model=list[IngredientSchema], status_code=HTTP_200_OK)
async def get_ingredients(db: AsyncSession = Depends(get_db)):
    repo = IngredientsRepository(db)
    return await repo.get_all()
