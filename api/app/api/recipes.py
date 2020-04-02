from typing import List

from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError
from fastapi import APIRouter, HTTPException
from orm.exceptions import NoMatch

from app.models.recipes import Recipe, RecipeDB, RecipeSchema


router = APIRouter()


@router.post("/", response_model=RecipeDB, status_code=201)
async def add_recipe(sid: int, payload: RecipeSchema):
    try:
        recipe = await Recipe.objects.create(
            name=payload.name, url=payload.url, image=payload.image, sid=sid
        )
    except ForeignKeyViolationError:
        raise HTTPException(status_code=404, detail="Source does not exist")
    except UniqueViolationError:
        raise HTTPException(status_code=400, detail="Recipe url already exists")

    response_object = {
        "id": recipe.pk,
        "name": payload.name,
        "url": payload.url,
        "image": payload.image,
        "sid": sid,
    }
    return response_object


@router.get("/{id}/", response_model=RecipeDB, status_code=200)
async def get_recipe(sid: int, id: int):
    try:
        recipe = await Recipe.objects.get(sid=sid, id=id)
    except NoMatch:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.get("/", response_model=List[RecipeDB], status_code=200)
async def get_recipes(sid: int):
    return await Recipe.objects.get(sid=sid).all()


@router.put("/{id}/", response_model=RecipeDB, status_code=200)
async def update_recipe(sid: int, id: int, payload: RecipeSchema):
    recipe = await get_recipe(sid, id)
    await recipe.update(name=payload.name, url=payload.url, image=payload.image)
    return recipe


@router.delete("/{id}/", response_model=RecipeDB, status_code=200)
async def remove_recipe(sid: int, id: int):
    recipe = await get_recipe(sid, id)
    await recipe.delete()
    return recipe
