import meilisearch_python_async
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, paginate
from loguru import logger
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.requests import Request
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from app.core.exceptions import AlreadyExists, DoesNotExist
from app.db.dal.ingredients import IngredientsDAL
from app.db.dal.recipes import RecipesDAL
from app.db.session import get_db, get_mc
from app.schemas.ingredients import InIngredientSchema
from app.schemas.recipes import InRecipeSchema, InRecipeSchemaRaw, RecipeSchema

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
    req: Request,
    payload: InRecipeSchemaRaw,
    db: AsyncSession = Depends(get_db),
    mc: meilisearch_python_async.Client = Depends(get_mc),
):
    _payload = extract_ingredients(req, payload)

    try:
        recipe = await RecipesDAL(db).create(_payload)
    except AlreadyExists:
        raise HTTPException(HTTP_400_BAD_REQUEST, "Recipe exists")

    await register_recipe_ingredients(db, recipe)
    await mc.index("recipes").add_documents(documents=[recipe.dict()], primary_key="id")

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


async def register_recipe_ingredients(db: AsyncSession, recipe: RecipeSchema) -> None:
    for ingredient in recipe.ingredients["items"]:
        payload = InIngredientSchema(ingredient=ingredient)
        try:
            await IngredientsDAL(db).create(payload)
        except AlreadyExists:
            logger.info(f"{ingredient!r} already exists in DB")
