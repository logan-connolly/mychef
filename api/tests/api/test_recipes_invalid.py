from json import dumps

import pytest


source = dict(name="Source", url="http://source.com")
sid: int = None


class TestRecipeInvalid:
    @pytest.mark.asyncio
    async def test_create_source(self, event_loop, server, host, session):
        global source
        global sid
        async with session.post(f"{host}/sources/", data=dumps(source)) as resp:
            assert resp.status == 201
            response = await resp.json()
            sid = response["id"]
            source.update({"id": sid, "url": "source.com"})
            assert response == source

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "recipe, code",
        [
            (dict(name="no url or image"), 422),
            (dict(name="Bad url", url="url", image="http://image.com"), 422),
            (dict(name="Bad image url", url="http://url.com", image="image"), 422),
        ],
    )
    async def test_add_recipe_invalid(
        self, event_loop, server, host, session, recipe, code
    ):
        async with session.post(
            f"{host}/sources/1/recipes/", data=dumps(recipe)
        ) as resp:
            assert resp.status == code

    @pytest.mark.asyncio
    async def test_get_recipe_invalid(self, event_loop, server, host, session):
        global sid
        async with session.get(f"{host}/sources/{sid}/recipes/0") as resp:
            assert resp.status == 404

    @pytest.mark.asyncio
    async def test_get_recipes_invalid(self, event_loop, server, host, session):
        async with session.get(f"{host}/sources/0/recipes/") as resp:
            assert resp.status == 404

    @pytest.mark.asyncio
    async def test_update_recipe_invalid(self, event_loop, server, host, session):
        global sid
        async with session.put(
            f"{host}/sources/{sid}/recipes/0", data=dumps(dict())
        ) as resp:
            assert resp.status == 404

    @pytest.mark.asyncio
    async def test_remove_recipe_invalid(self, event_loop, server, host, session):
        global sid
        async with session.delete(f"{host}/sources/{sid}/recipes/0") as resp:
            assert resp.status == 404

    @pytest.mark.asyncio
    async def test_remove_source(self, event_loop, server, host, session):
        global sid
        async with session.delete(f"{host}/sources/{sid}") as resp:
            assert resp.status == 200
