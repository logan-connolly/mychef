from typing import List

from app.models.sources import SourceDB, SourceSchema
from app.db import sources, database
from fastapi import APIRouter, HTTPException


router = APIRouter()


@router.post("/", response_model=SourceDB, status_code=201)
async def add_source(payload: SourceSchema):
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
        if await url_exists(payload.url.host):
            raise HTTPException(status_code=400, detail="URL already exists")

        query = sources.insert().values(name=payload.name, url=payload.url.host)
        return await database.execute(query=query)

    @staticmethod
    async def get(id: int):
        query = sources.select().where(id == sources.c.id)
        return await database.fetch_one(query=query)

    @staticmethod
    async def get_all():
        query = sources.select()
        return await database.fetch_all(query=query)

    @staticmethod
    async def put(id: int, payload: SourceSchema):
        query = (
            sources
            .update()
            .where(id == sources.c.id)
            .values(name=payload.name, url=payload.url.host)
            .returning(sources.c.id)
        )
        return await database.execute(query=query)

    @staticmethod
    async def delete(id: int):
        query = sources.delete().where(id == sources.c.id)
        return await database.execute(query=query)


async def url_exists(url: str):
    query = sources.select().where(url == sources.c.url)
    return await database.fetch_one(query=query)
