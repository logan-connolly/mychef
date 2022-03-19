import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, paginate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.requests import Request
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from app.core.config import settings
from app.core.exceptions import DoesNotExist
from app.db.dal.recipes import RecipesDAL
from app.db.session import get_db
from app.schemas.recipes import InRecipeSchema, InRecipeSchemaRaw, RecipeSchema

from .ingredients import InIngredientSchema, add_ingredient

router = APIRouter()

Ingredients = dict[str, list[str]]


def extract_ingredients(req: Request, payload: InRecipeSchemaRaw) -> InRecipeSchema:
    """Accept a recipe text and extract ingredients detected through NER model"""
    try:
        found_ingreds = {"items": req.app.state.extractor.extract(payload.ingredients)}
    except AttributeError as err:
        raise HTTPException(HTTP_404_NOT_FOUND, "Ingredient model missing") from err

    return InRecipeSchema(
        name=payload.name,
        source_id=payload.source_id,
        url=payload.url,
        image=payload.image,
        ingredients=found_ingreds,
    )


@router.post("/", response_model=RecipeSchema, status_code=HTTP_201_CREATED)
async def add_recipe(
    req: Request, payload: InRecipeSchemaRaw, db: AsyncSession = Depends(get_db)
):
    _payload = extract_ingredients(req, payload)

    try:
        recipe = await RecipesDAL(db).create(_payload)
    except IntegrityError:
        raise HTTPException(HTTP_400_BAD_REQUEST, "Recipe exists")

    await send_off_recipe(db, recipe)
    return recipe


@router.get("/{recipe_id}/", response_model=RecipeSchema, status_code=HTTP_200_OK)
async def get_recipe(recipe_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await RecipesDAL(db).get_by_id(recipe_id)
    except DoesNotExist:
        raise HTTPException(HTTP_404_NOT_FOUND, "Recipe not found")


@router.get("/", response_model=Page[RecipeSchema], status_code=HTTP_200_OK)
async def get_recipes(db: AsyncSession = Depends(get_db)):
    recipes = await RecipesDAL(db).get_all()
    return paginate(recipes)


# TODO: move this out of module and trigger on event
async def send_off_recipe(db: AsyncSession, recipe: RecipeSchema) -> None:
    """Asynchronously send off recipe to ingredients and meilisearch endpoints"""

    async def update_ingredients():
        for ingredient in recipe.ingredients["items"]:
            await add_ingredient(InIngredientSchema(ingredient=ingredient), db=db)

    async def update_meili_recipe_index() -> None:
        async with httpx.AsyncClient() as client:
            await client.post(settings.search_url, json=[recipe.dict()])

    await update_ingredients()
    await update_meili_recipe_index()
