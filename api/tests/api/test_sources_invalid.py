from json import dumps

import pytest


class TestSourceInvalid:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "payload, code",
        [
            (dict(name="no url"), 422),
            (dict(name="bad url", url="url"), 422),
            (dict(name="no http", url="url.com"), 422),
        ],
    )
    async def test_add_source_invalid(
        self, event_loop, server, host, session, payload, code
    ):
        async with session.post(f"{host}/sources/", data=dumps(payload)) as resp:
            assert resp.status == code

    @pytest.mark.asyncio
    async def test_get_source_invalid(self, event_loop, host, server, session):
        async with session.get(f"{host}/sources/0") as resp:
            assert resp.status == 404

    @pytest.mark.asyncio
    async def test_get_sources_invalid(self, event_loop, host, server, session):
        async with session.get(f"{host}/sources/") as resp:
            assert resp.status == 404

    @pytest.mark.asyncio
    async def test_update_source_invalid(self, event_loop, server, host, session):
        async with session.put(f"{host}/sources/0", data=dumps(dict())) as resp:
            assert resp.status == 404

    @pytest.mark.asyncio
    async def test_remove_source_invalid(self, event_loop, server, host, session):
        async with session.delete(f"{host}/sources/0") as resp:
            assert resp.status == 404
