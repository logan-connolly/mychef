from fastapi import FastAPI
from app.api import sources, recipes
from app.db import engine, metadata, database


metadata.create_all(engine)


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(sources.router, prefix="/sources", tags=["sources"])
app.include_router(recipes.router, prefix="/sources/{sid}/recipes", tags=["recipes"])
