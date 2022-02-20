from app.db.repositories.recipes import RecipesRepository
from app.schemas.recipes import InRecipeSchema, RecipeSchema

import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.requests import Request
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
)

from app.core.config import settings

from app.db.repositories.recipes import RecipesRepository
from app.db.session import get_db
from app.schemas.recipes import InRecipeSchema, InRecipeSchemaRaw, RecipeSchema

from .ingredients import InIngredientSchema, add_ingredient

router = APIRouter()

Ingredients = dict[str, list[str]]


def extract_ingredients(req: Request, p: InRecipeSchemaRaw) -> InRecipeSchema:
    """Accept a recipe text and extract ingredients detected through NER model"""
    try:
        d = {"items": req.app.state.ingredient_model.extract(p.ingredients)}
    except AttributeError as err:
        raise HTTPException(HTTP_404_NOT_FOUND, "Ingredient model missing") from err

    return RecipeSchema(name=p.name, url=p.url, image=p.image, ingredients=d)


@router.post("/", response_model=RecipeSchema, status_code=HTTP_201_CREATED)
async def add_recipe(
    req: Request, payload: InRecipeSchemaRaw, db: AsyncSession = Depends(get_db)
):
    repo = RecipesRepository(db)
    _payload = extract_ingredients(req, payload)
    recipe = await repo.create(_payload)
    await send_off_recipe(recipe)
    return recipe


@router.get("/{recipe_id}/", response_model=RecipeSchema, status_code=HTTP_200_OK)
async def get_recipe(recipe_id: int, db: AsyncSession = Depends(get_db)):
    repo = RecipesRepository(db)
    return await repo.get_by_id(recipe_id)


@router.get("/", response_model=Page[RecipeSchema], status_code=HTTP_200_OK)
async def get_recipes(db: AsyncSession = Depends(get_db)):
    repo = RecipesRepository(db)
    recipes = await repo.get_all()
    return paginate(recipes)


# TODO: move this out of module and trigger on event
async def send_off_recipe(recipe: RecipeSchema) -> None:
    """Asynchronously send off recipe to ingredients and meilisearch endpoints"""

    async def update_ingredients():
        for ingredient in recipe.ingredients["items"]:
            await add_ingredient(InIngredientSchema(ingredient=ingredient))

    async def update_meili_recipe_index() -> None:
        async with httpx.AsyncClient() as client:
            await client.post(f"{settings.search_url}", json=recipe.dict())

    await update_ingredients()
    await update_meili_recipe_index()
