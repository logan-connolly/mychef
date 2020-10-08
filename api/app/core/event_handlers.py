from fastapi import FastAPI

from app.db.database import database
from app.services.models import load_model


async def start_app_handler(app: FastAPI) -> None:
    app.state.model = load_model()
    await database.connect()


async def stop_app_handler(app: FastAPI) -> None:
    app.state.model = None
    await database.disconnect()
