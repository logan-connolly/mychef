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


@router.get("/", response_model=List[schemas.SourceDB], status_code=HTTP_200_OK)
async def get_sources(domain: Optional[str] = None):
    sources = await (
        models.Source.objects.filter(url__contains=domain).all()
        if domain
        else models.Source.objects.all()
    )
    if not sources:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No sources found")
    return sources


@router.post("/", response_model=schemas.SourceDB, status_code=HTTP_201_CREATED)
async def add_source(payload: schemas.SourceCreate):
    try:
        return await models.Source.objects.create(
            name=payload.name, url=payload.url.host
        )
    except UniqueViolationError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Source exists")


@router.get("/{id}/", response_model=schemas.SourceDB, status_code=HTTP_200_OK)
async def get_source(id: int):
    try:
        return await models.Source.objects.get(id=id)
    except NoMatch:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Source not found")


@router.put("/{id}/", response_model=schemas.SourceDB, status_code=HTTP_200_OK)
async def update_source(id: int, payload: schemas.SourceUpdate):
    source = await get_source(id)
    payload = {k: v for k, v in payload.dict().items() if v is not None}
    await source.update(**payload)
    return source


@router.delete("/{id}/", response_model=schemas.SourceDB, status_code=HTTP_200_OK)
async def remove_source(id: int):
    source = await get_source(id)
    await source.delete()
    return source
