from typing import Any, Dict
from fastapi import APIRouter

from .endpoints import ingredients, recipes, sources


api_router = APIRouter()

kwargs: Dict[str, Dict[str, Any]] = {
    "ingredients": dict(prefix="/ingredients", tags=["ingredients"]),
    "recipes": dict(prefix="/sources/{sid}/recipes", tags=["recipes"]),
    "sources": dict(prefix="/sources", tags=["sources"]),
}

api_router.include_router(ingredients.router, **kwargs["ingredients"])
api_router.include_router(sources.router, **kwargs["sources"])
api_router.include_router(recipes.router, **kwargs["recipes"])
