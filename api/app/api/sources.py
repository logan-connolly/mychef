from typing import List

from app.models.sources import Source, SourceDB, SourceSchema
from fastapi import APIRouter, HTTPException


router = APIRouter()


@router.post("/", response_model=SourceDB, status_code=201)
async def add_source(payload: SourceSchema):
    if not await Source.objects.get(url=payload.url):
        raise HTTPException(status_code=400, detail="URL already exists")

    source_id = await CRUD.post(payload)

    response_object = {
        "id": source_id,
        "name": payload.name,
        "url": payload.url.host,
    }
    return response_object


@router.get("/{id}/", response_model=SourceDB, status_code=200)
async def get_source(id: int):
    source = await CRUD.get(id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


@router.get("/", response_model=List[SourceDB], status_code=200)
async def list_sources():
    return await CRUD.get_all()


@router.put("/{id}/", response_model=SourceDB, status_code=200)
async def update_source(id: int, payload: SourceSchema):
    source = await CRUD.get(id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    source_id = await CRUD.put(id, payload)

    response_object = {
        "id": source_id,
        "name": payload.name,
        "url": payload.url,
    }
    return response_object


@router.delete("/{id}/", response_model=SourceDB, status_code=200)
async def remove_source(id: int):
    source = await CRUD.get(id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    await CRUD.delete(id)
    return source


class CRUD:
    @staticmethod
    async def post(payload: SourceSchema):
        return await Source.objects.create(name=payload.name, url=payload.url.host)

    @staticmethod
    async def get(id: int):
        return await Source.objects.get(id=id)

    @staticmethod
    async def get_all():
        return await Source.objects.all()

    @staticmethod
    async def put(id: int, payload: SourceSchema):
        source = await Source.objects.get(id)
        return await source.update(name=payload.name, url=payload.url)

    @staticmethod
    async def delete(id: int):
        source = await Source.objects.get(id)
        return await source.delete()
