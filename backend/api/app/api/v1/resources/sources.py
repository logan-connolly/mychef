from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from app.core.exceptions import AlreadyExists, DoesNotExist
from app.db.dal.sources import SourcesDAL
from app.db.session import get_db
from app.schemas.sources import InSourceSchema, SourceSchema

router = APIRouter()


@router.post("/", response_model=SourceSchema, status_code=HTTP_201_CREATED)
async def add_source(payload: InSourceSchema, db: AsyncSession = Depends(get_db)):
    try:
        return await SourcesDAL(db).create(payload)
    except AlreadyExists:
        raise HTTPException(HTTP_400_BAD_REQUEST, "Source exists")


@router.get("/{source_id}/", response_model=SourceSchema, status_code=HTTP_200_OK)
async def get_source(source_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await SourcesDAL(db).get_by_id(source_id)
    except DoesNotExist:
        raise HTTPException(HTTP_404_NOT_FOUND, "Source not found")


@router.get("/", response_model=list[SourceSchema], status_code=HTTP_200_OK)
async def get_sources(db: AsyncSession = Depends(get_db)):
    return await SourcesDAL(db).get_all()
