from fastapi import FastAPI

from app.core.config import settings
from app.db.database import database
from app.services.models.ingredient import IngredientExtractor


async def start_app_handler(app: FastAPI) -> None:
    app.state.ingredient_model = IngredientExtractor(settings.api.ingredient_model)
    await database.connect()


async def stop_app_handler(app: FastAPI) -> None:
    app.state.ingredient_model = None
    await database.disconnect()
