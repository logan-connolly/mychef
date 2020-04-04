from typing import List, Optional

from asyncpg.exceptions import UniqueViolationError
from fastapi import APIRouter, HTTPException
from orm.exceptions import NoMatch

from ..models.recipes import Recipe, RecipeDB, RecipeSchema
from .sources import get_source


router = APIRouter()


@router.post("/", response_model=RecipeDB, status_code=201)
async def add_recipe(sid: int, payload: RecipeSchema):
    try:
        source = await get_source(id=sid)
        recipe = await Recipe.objects.create(
            source=source, name=payload.name, url=payload.url, image=payload.image
        )
    except UniqueViolationError:
        raise HTTPException(status_code=400, detail="Recipe url already exists")

    response_object = {
        "id": recipe.pk,
        "source": recipe.source.pk,
        "name": payload.name,
        "url": payload.url,
        "image": payload.image,
    }
    return response_object


@router.get("/{id}/", response_model=RecipeDB, status_code=200)
async def get_recipe(sid: int, id: int):
    try:
        recipe = await Recipe.objects.get(id=id, source=sid)
    except NoMatch:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.get("/", response_model=List[RecipeDB], status_code=200)
async def get_recipes(sid: int, limit: Optional[int] = None):
    recipes = await Recipe.objects.filter(source=sid).all()
    if not recipes:
        raise HTTPException(status_code=404, detail="No recipes found")
    if limit:
        return recipes[:limit]
    return recipes


@router.put("/{id}/", response_model=RecipeDB, status_code=200)
async def update_recipe(sid: int, id: int, payload: RecipeSchema):
    recipe = await get_recipe(sid=sid, id=id)
    await recipe.update(name=payload.name, url=payload.url, image=payload.image)
    return recipe


@router.delete("/{id}/", response_model=RecipeDB, status_code=200)
async def remove_recipe(sid: int, id: int):
    recipe = await get_recipe(sid=sid, id=id)
    await recipe.delete()
    return recipe
