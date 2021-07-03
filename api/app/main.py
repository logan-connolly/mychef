from fastapi import FastAPI
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware

from .api.api_v1.api import router
from .core.config import api_settings, settings
from .core.event_handlers import start_app_handler, stop_app_handler


def get_app():

    app = FastAPI(**api_settings)

    @app.on_event("startup")
    async def startup():
        await start_app_handler(app)

    @app.on_event("shutdown")
    async def shutdown():
        await stop_app_handler(app)

    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(router, prefix=settings.api.version)

    add_pagination(app)

    return app


app = get_app()
