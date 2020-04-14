import asyncio

from multiprocessing import Process

import aiohttp
import pytest
import uvicorn

from sqlalchemy import create_engine

from src import config, main, db


@pytest.yield_fixture(scope="module")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
async def server():
    kwargs = dict(host="127.0.0.1", port=5000, log_level="info")
    proc = Process(target=uvicorn.run, args=(main.app,), kwargs=kwargs, daemon=True)
    proc.start()
    await asyncio.sleep(0.2)
    yield
    proc.kill()


@pytest.fixture(scope="module")
async def session():
    async with aiohttp.ClientSession() as session:
        yield session


@pytest.fixture(scope="class")
def create_tables():
    test_url = config.settings.test_db_url
    engine = create_engine(test_url)
    db.metadata.create_all(engine)
    yield
    db.metadata.drop_all(engine)
