from typing import Any, Dict, List

from asyncpg.exceptions import UniqueViolationError
from fastapi import APIRouter, HTTPException
from orm.exceptions import NoMatch
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from app.models import Source
from app.schemas import SourceDB, SourceCreate, SourceUpdate

router = APIRouter()


@router.get("/", response_model=List[SourceDB], status_code=HTTP_200_OK)
async def get_sources():
    sources = await Source.objects.all()
    if not sources:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="No sources found")
    return sources


@router.post("/", response_model=SourceDB, status_code=HTTP_201_CREATED)
async def add_source(payload: SourceCreate):
    try:
        return await Source.objects.create(name=payload.name, url=payload.url.host)
    except UniqueViolationError as err:
        raise HTTPException(HTTP_400_BAD_REQUEST, detail="Source exists") from err


@router.get("/{id}/", response_model=SourceDB, status_code=HTTP_200_OK)
async def get_source(id: int):
    try:
        return await Source.objects.get(id=id)
    except NoMatch as err:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="Source not found") from err


@router.put("/{id}/", response_model=SourceDB, status_code=HTTP_200_OK)
async def update_source(id: int, payload: SourceUpdate):
    source = await get_source(id)
    updates: Dict[str, Any] = {k: v for k, v in payload.dict().items() if v is not None}
    return await source.update(**updates)


@router.delete("/{id}/", response_model=SourceDB, status_code=HTTP_200_OK)
async def remove_source(id: int):
    source = await get_source(id)
    await source.delete()
    return source
