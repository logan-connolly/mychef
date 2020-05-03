from fastapi import APIRouter

from .endpoints import sources, recipes

api_router = APIRouter()
api_router.include_router(sources.router, prefix="/sources", tags=["sources"])
api_router.include_router(
    recipes.router, prefix="/sources/{sid}/recipes", tags=["recipes"]
)
