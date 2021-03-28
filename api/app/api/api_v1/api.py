from fastapi import APIRouter

from .endpoints import ingredients, recipes, sources

router = APIRouter()

router.include_router(ingredients.router, prefix="/ingredients", tags=["ingredients"])
router.include_router(sources.router, prefix="/sources", tags=["sources"])
router.include_router(recipes.router, prefix="/sources/{sid}/recipes", tags=["recipes"])
