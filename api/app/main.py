from fastapi import FastAPI

from .api.api_v1.api import api_router
from .core.config import api_settings, settings
from .core.event_handlers import start_app_handler, stop_app_handler
from .db.database import engine, metadata


metadata.create_all(engine)


def get_app():

    app = FastAPI(**api_settings)

    @app.on_event("startup")
    async def startup():
        await start_app_handler(app)

    @app.on_event("shutdown")
    async def shutdown():
        await stop_app_handler(app)

    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app


app = get_app()
