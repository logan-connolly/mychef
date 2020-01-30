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
         "url": payload.url,
     }
    return response_object


@router.get("/{id}/", response_model=SourceDB, status_code=200)
async def get_source(id: int):
    source = await CRUD.get(id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


class CRUD:
    @classmethod
    async def post(payload: SourceSchema):
        query = sources.insert().values(name=payload.name, url=payload.url)
        return await database.execute(query=query)

    @classmethod
    async def get(id: int):
        query = sources.select().where(id == sources.c.id)
        return await database.fetch_one(query=query)

