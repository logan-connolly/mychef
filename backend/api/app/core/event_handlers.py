from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.api.v1.router import router
from app.core.config import settings
from app.core.middleware import add_cors_middleware
from app.db.database import database
from app.services.models.ingredient import IngredientExtractor


async def start_app_handler(app: FastAPI) -> None:
    app.include_router(router, prefix=settings.api.version)
    app.state.ingredient_model = IngredientExtractor()
    add_pagination(app)
    add_cors_middleware(app)
    await database.connect()


async def stop_app_handler(app: FastAPI) -> None:
    app.state.ingredient_model = None
    await database.disconnect()
