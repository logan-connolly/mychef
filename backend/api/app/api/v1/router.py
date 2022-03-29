from fastapi import APIRouter

from app.api.v1.resources import ingredients, recipes, sources

router = APIRouter()

router.include_router(ingredients.router, prefix="/ingredients", tags=["ingredients"])
router.include_router(sources.router, prefix="/sources", tags=["sources"])
router.include_router(recipes.router, prefix="/recipes", tags=["recipes"])
