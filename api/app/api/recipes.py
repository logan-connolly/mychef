from typing import List

from app.models.recipes import RecipeDB, RecipeSchema
from app.db import recipes, database
from fastapi import APIRouter, HTTPException


router = APIRouter()


@router.post("/", response_model=RecipeDB, status_code=201)
async def add_recipe(sid: int, payload: RecipeSchema):
    if await url_exists(payload.url):
        raise HTTPException(status_code=400, detail="URL already exists")

    recipe_id = await CRUD.post(sid, payload)

    response_object = {
        "id": recipe_id,
        "name": payload.name,
        "url": payload.url,
        "image": payload.image,
        "sid": sid,
    }
    return response_object


@router.get("/{id}/", response_model=RecipeDB, status_code=200)
async def get_recipe(sid: int, id: int):
    recipe = await CRUD.get(sid, id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.get("/", response_model=List[RecipeDB], status_code=200)
async def list_recipes(sid: int):
    return await CRUD.get_all(sid)


@router.put("/{id}/", response_model=RecipeDB, status_code=200)
async def update_recipe(sid: int, id: int, payload: RecipeSchema):
    recipe = await CRUD.get(sid, id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    recipe_id = await CRUD.put(sid, id, payload)

    response_object = {
        "id": recipe_id,
        "name": payload.name,
        "url": payload.url,
        "image": payload.image,
        "sid": sid
    }
    return response_object


@router.delete("/{id}/", response_model=RecipeDB, status_code=200)
async def remove_recipe(sid: int, id: int):
    recipe = await CRUD.get(sid, id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    await CRUD.delete(sid, id)

    return recipe


class CRUD:
    @staticmethod
    async def post(sid:int, payload: RecipeSchema):
        query = recipes.insert().values(name=payload.name, url=payload.url,
                                        image=payload.image, sid=sid)
        return await database.execute(query=query)

    @staticmethod
    async def get(sid: int, id: int):
        query = recipes.select().where(id == recipes.c.id)
        return await database.fetch_one(query=query)

    @staticmethod
    async def get_all(sid: int):
        query = recipes.select().where(sid == recipes.c.sid)
        return await database.fetch_all(query=query)

    @staticmethod
    async def put(sid: int, id: int, payload: RecipeSchema):
        query = (
            recipes
            .update()
            .where(id == recipes.c.id)
            .values(name=payload.name, url=payload.url, image=payload.image)
            .returning(recipes.c.id)
        )
        return await database.execute(query=query)

    @staticmethod
    async def delete(sid: int, id: int):
        query = (
            recipes
            .delete()
            .where(sid == recipes.c.sid)
            .where(id == recipes.c.id)
        )
        return await database.execute(query=query)


async def url_exists(url: str):
    query = recipes.select().where(url == recipes.c.url)
    return await database.fetch_one(query=query)
