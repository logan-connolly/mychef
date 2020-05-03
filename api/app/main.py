from fastapi import FastAPI

from .api.api_v1.api import api_router
from .core.config import settings
from .db.database import database, engine, metadata


def get_app():

    app = FastAPI(title="mychef", openapi_url=f"{settings.API_V1_STR}/openapi.json")

    metadata.create_all(engine)

    @app.on_event("startup")
    async def startup():
        await database.connect()

    @app.on_event("shutdown")
    async def shutdown():
        await database.disconnect()

    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app


app = get_app()
