from fastapi import FastAPI

from app.core.config import settings
from app.core.event_handlers import start_app_handler, stop_app_handler


def get_app():

    app = FastAPI(
        title="MyChef", description="Recipe recommender app", debug=settings.debug
    )

    @app.on_event("startup")
    async def startup():
        await start_app_handler(app)

    @app.on_event("shutdown")
    async def shutdown():
        await stop_app_handler(app)

    return app


app = get_app()
