from fastapi import FastAPI

from .api import sources, recipes
from .db import database


def get_app():

    app = FastAPI()

    @app.on_event("startup")
    async def startup():
        await database.connect()

    @app.on_event("shutdown")
    async def shutdown():
        await database.disconnect()

    return app


app = get_app()


app.include_router(sources.router, prefix="/sources", tags=["sources"])
app.include_router(recipes.router, prefix="/sources/{sid}/recipes", tags=["recipes"])
