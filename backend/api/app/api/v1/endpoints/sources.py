from app.core.exceptions import DoesNotExist
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from app.db.repositories.sources import SourcesRepository
from app.db.session import get_db
from app.schemas.sources import InSourceSchema, SourceSchema

router = APIRouter()


@router.post("/", response_model=SourceSchema, status_code=HTTP_201_CREATED)
async def add_source(payload: InSourceSchema, db: AsyncSession = Depends(get_db)):
    repo = SourcesRepository(db)
    try:
        return await repo.create(payload)
    except IntegrityError:
        raise HTTPException(HTTP_400_BAD_REQUEST, "Source exists")


@router.get("/{source_id}/", response_model=SourceSchema, status_code=HTTP_200_OK)
async def get_source(source_id: int, db: AsyncSession = Depends(get_db)):
    repo = SourcesRepository(db)
    try:
        return await repo.get_by_id(source_id)
    except DoesNotExist:
        raise HTTPException(HTTP_404_NOT_FOUND, "Source not found")


@router.get("/", response_model=list[SourceSchema], status_code=HTTP_200_OK)
async def get_sources(db: AsyncSession = Depends(get_db)):
    repo = SourcesRepository(db)
    return await repo.get_all()
