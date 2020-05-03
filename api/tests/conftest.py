import asyncio

from multiprocessing import Process

import aiohttp
import pytest
import uvicorn

from app import main
from app.core.config import settings


@pytest.fixture(scope="module")
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
def host():
    yield f"http://127.0.0.1:5000{settings.API_V1_STR}"


@pytest.fixture(scope="module")
async def session():
    async with aiohttp.ClientSession() as session:
        yield session
