from typing import List

from asyncpg.exceptions import ForeignKeyViolationError
from fastapi import APIRouter, HTTPException

from app.models.recipes import Recipe, RecipeDB, RecipeSchema


router = APIRouter()


@router.post("/", response_model=RecipeDB, status_code=201)
async def add_recipe(sid: int, payload: RecipeSchema):
    if not await Recipe.objects.get(url=payload.url):
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
        return await Recipe.objects.create(name=payload.name, url=payload.url, sid=sid)

    @staticmethod
    async def get(sid: int, id: int):
        return await Recipe.objects.get(sid=sid, id=id)

    @staticmethod
    async def get_all(sid: int):
        return await Recipe.objects.all()

    @staticmethod
    async def put(sid: int, id: int, payload: RecipeSchema):
        recipe = await Recipe.objects.get(sid=sid, id=id)
        return await recipe.update(
            name=payload.name, url=payload.url, image=payload.image
        )

    @staticmethod
    async def delete(sid: int, id: int):
        recipe = await Recipe.objects.get(sid=sid, id=id)
        return await recipe.delete()
