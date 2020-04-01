from typing import List

from asyncpg.exceptions import ForeignKeyViolationError
from fastapi import APIRouter, HTTPException

from app.models.recipes import RecipeDB, RecipeSchema
from app.db import session
from app.models.recipes import Recipe


router = APIRouter()


@router.post("/", response_model=RecipeDB, status_code=201)
async def add_recipe(sid: int, payload: RecipeSchema):
    url_check = session.query(Recipe.id).filter_by(url=payload.url).scalar()
    if await url_check is None:
        raise HTTPException(status_code=400, detail="URL already exists")

    try:
        recipe_id = await CRUD.post(sid, payload)
    except ForeignKeyViolationError:
        raise HTTPException(status_code=404, detail="Source does not exist")

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
    recipes = await CRUD.get_all(sid)
    if not recipes:
        raise HTTPException(status_code=404, detail="No recipes found for source")
    return recipes


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
        "sid": sid,
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
    async def post(sid: int, payload: RecipeSchema):
        recipe = Recipe(
            name=payload.name, url=payload.url, image=payload.image, sid=sid
        )
        recipe.add()
        recipe.commit()
        return await recipe.id

    @staticmethod
    async def get(sid: int, id: int):
        return await session.query(Recipe).filter_by(sid=sid, id=id).first()

    @staticmethod
    async def get_all(sid: int):
        return await session.query(Recipe).filter_by(sid=sid)

    @staticmethod
    async def put(sid: int, id: int, payload: RecipeSchema):
        recipe = session.query(Recipe).filter_by(id=id, sid=sid)
        recipe.name = payload.name
        recipe.url = payload.url
        recipe.image = payload.image
        session.commit()
        return await recipe.id

    @staticmethod
    async def delete(sid: int, id: int):
        session.query(Recipe).filter_by(sid=sid, id=id).delete()
        return await session.commit()
