from fastapi import FastAPI

from app.core.config import api_settings
from app.core.event_handlers import start_app_handler, stop_app_handler


def get_app():

    app = FastAPI(**api_settings)

    @app.on_event("startup")
    async def startup():
        await start_app_handler(app)

    @app.on_event("shutdown")
    async def shutdown():
        await stop_app_handler(app)

    return app


app = get_app()
