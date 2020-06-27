from json import dumps

import pytest


source = dict(name="Example", url="http://example.com")


class TestSource:
    @pytest.mark.asyncio
    async def test_add_source(self, event_loop, server, host, session):
        global source
        async with session.post(f"{host}/sources/", data=dumps(source)) as resp:
            assert resp.status == 201
            response = await resp.json()
            source.update({"id": response.get("id"), "url": "example.com"})
            assert response == source

    @pytest.mark.asyncio
    async def test_get_source(self, event_loop, server, host, session):
        global source
        async with session.get(f"{host}/sources/{source.get('id')}") as resp:
            assert resp.status == 200
            assert await resp.json() == source

    @pytest.mark.asyncio
    async def test_get_sources(self, event_loop, server, host, session):
        global source
        async with session.get(f"{host}/sources/") as resp:
            assert resp.status == 200
            sources = await resp.json()
            assert source in sources

    @pytest.mark.asyncio
    async def test_update_source(self, event_loop, server, host, session):
        global source
        new_url = "http://newexample.com"
        source["url"] = new_url
        async with session.put(
            f"{host}/sources/{source.get('id')}", data=dumps(dict(url=new_url))
        ) as resp:
            assert resp.status == 200
            assert await resp.json() == source

    @pytest.mark.asyncio
    async def test_remove_source(self, event_loop, server, host, session):
        global source
        async with session.delete(f"{host}/sources/{source.get('id')}") as resp:
            assert resp.status == 200
            assert await resp.json() == source
