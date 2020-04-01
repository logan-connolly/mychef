from typing import List

from app.models.sources import SourceDB, SourceSchema
from app.db import session
from app.models.sources import Source
from fastapi import APIRouter, HTTPException


router = APIRouter()


@router.post("/", response_model=SourceDB, status_code=201)
async def add_source(payload: SourceSchema):
    url_check = session.query(Source.id).filter_by(url=payload.url).scalar()
    if await url_check is None:
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
        source = Source(name=payload.name, url=payload.url.host).add()
        session.add(source.add)
        session.commit()
        return await source.id

    @staticmethod
    async def get(id: int):
        return await session.query(Source).filter_by(id=id).first()

    @staticmethod
    async def get_all():
        return await session.query(Source).all()

    @staticmethod
    async def put(id: int, payload: SourceSchema):
        source = session.query(Source).filter_by(id=id)
        source.name = payload.name
        source.url = payload.url.host
        session.commit()
        return await source.id

    @staticmethod
    async def delete(id: int):
        session.query(Source).filter_by(id=id).delete()
        return await session.commit()
