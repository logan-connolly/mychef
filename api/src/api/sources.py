from typing import List

from asyncpg.exceptions import UniqueViolationError
from fastapi import APIRouter, HTTPException
from orm.exceptions import NoMatch
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from ..models.sources import Source, SourceDB, SourceSchema


router = APIRouter()


@router.post("/", response_model=SourceDB, status_code=HTTP_201_CREATED)
async def add_source(payload: SourceSchema):
    try:
        source = await Source.objects.create(name=payload.name, url=payload.url.host)
    except UniqueViolationError:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Source url already exists"
        )

    response_object = {
        "id": source.pk,
        "name": payload.name,
        "url": payload.url.host,
    }
    return response_object


@router.get("/{id}/", response_model=SourceDB, status_code=HTTP_200_OK)
async def get_source(id: int):
    try:
        source = await Source.objects.get(id=id)
    except NoMatch:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Source not found")
    return source


@router.get("/", response_model=List[SourceDB], status_code=HTTP_200_OK)
async def get_sources(domain: str = None):
    if domain:
        sources = await Source.objects.filter(url__contains=domain).all()
        if not sources:
            message = f"No sources matching '{domain}' domain pattern"
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=message)
        return sources

    sources = await Source.objects.all()
    if not sources:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Could not find any sources"
        )
    return sources


@router.put("/{id}/", response_model=SourceDB, status_code=HTTP_200_OK)
async def update_source(id: int, payload: SourceSchema):
    source = await get_source(id)
    await source.update(name=payload.name, url=payload.url)
    return source


@router.delete("/{id}/", response_model=SourceDB, status_code=HTTP_200_OK)
async def remove_source(id: int):
    source = await get_source(id)
    await source.delete()
    return source
