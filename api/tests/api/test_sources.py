import json

import aiohttp
import pytest


host = "http://127.0.0.1:5000"


@pytest.mark.usefixtures("create_tables")
class TestSource:

    @pytest.mark.asyncio
    async def test_add_source(self, event_loop, server, session):
        payload = dict(name="Example", url="http://example.com")
        dumps = json.dumps(payload)

        async with session.post(f"{host}/sources/", data=dumps) as resp:
            data = await resp.json()
            status = resp.status

        assert status == 201
        assert data == dict(id=1, name="Example", url="example.com")

    @pytest.mark.asyncio
    async def test_get_source(self, event_loop, server, session):
        expected = dict(id=1, name="Example", url="example.com")

        async with session.get(f"{host}/sources/1") as resp:
            data = await resp.json()
            status = resp.status

        assert status == 200
        assert data == expected

    @pytest.mark.asyncio
    async def test_get_sources(self, event_loop, server, session):
        expected = [{"id": 1, "name": "Example", "url": "example.com"}]

        async with session.get(f"{host}/sources/") as resp:
            data = await resp.json()
            status = resp.status

        assert status == 200
        assert data == expected

    @pytest.mark.asyncio
    async def test_update_source(self, event_loop, server, session):
        payload = dict(name="Example2", url="http://example2.com")
        dumps = json.dumps(payload)

        async with session.put(f"{host}/sources/1", data=dumps) as resp:
            data = await resp.json()
            status = resp.status

        assert status == 200
        payload.update({"id": 1})
        assert data == payload

    @pytest.mark.asyncio
    async def test_remove_source(self, event_loop, server, session):
        expected = dict(id=1, name="Example2", url="http://example2.com")

        async with session.delete(f"{host}/sources/1") as resp:
            data = await resp.json()
            status = resp.status

        assert status == 200
        assert data == expected


@pytest.mark.usefixtures("create_tables")
class TestSourceInvalid:

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "payload, code",
        [
            [{"name": "No URL"}, 422],
            [{"name": "Not URL", "url": "notaurl"}, 422],
            [{"name": "No http", "url": "notaurl.com"}, 422],
        ]
    )
    async def test_add_source_invalid(self, event_loop, server, session, payload, code):
        dumps = json.dumps(payload)
        async with session.post(f"{host}/sources/", data=dumps) as resp:
            status = resp.status

        assert status == code

    @pytest.mark.asyncio
    async def test_get_source_invalid(self, event_loop, server, session):
        async with session.get(f"{host}/sources/999") as resp:
            status = resp.status

        assert status == 404

    @pytest.mark.asyncio
    async def test_get_sources_invalid(self, event_loop, server, session):
        async with session.get(f"{host}/sources/") as resp:
            status = resp.status

        assert status == 404

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "id, payload, code",
        [
            [1, {}, 422],
            [1, {"name": "only name"}, 422],
            [1, {"url": "http://example.com"}, 422],
            [999, {"name": "bad id", "url": "http://example.com"}, 404],
        ],
    )
    async def test_update_source_invalid(self, event_loop, server, session, id, payload, code):
        dumps = json.dumps(payload)
        async with session.put(f"{host}/sources/{id}", data=dumps) as resp:
            status = resp.status

        assert status == code

    @pytest.mark.asyncio
    async def test_remove_source_invalid(self, event_loop, server, session):
        async with session.delete(f"{host}/sources/1") as resp:
            status = resp.status

        assert status == 404
