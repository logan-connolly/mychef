from pathlib import Path
from typing import Callable

from fastapi import FastAPI
from loguru import logger

from app.db.database import database
from app.core.config import settings
from app.services.models import IngredientExtractor


async def start_app_handler(app: FastAPI) -> Callable:
    model_dir = Path("/app/models")
    try:
        model = IngredientExtractor(model_dir / settings.MODEL)
    except OSError:
        logger.warning("Could not find model.")
        model = IngredientExtractor()
    finally:
        app.state.model = model
        logger.info(f"{model} loaded and attached to app.")
        await database.connect()


async def stop_app_handler(app: FastAPI) -> Callable:
    app.state.model = None
    await database.disconnect()
