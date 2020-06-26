from json import dumps

import pytest

source = dict(name="Source", url="http://source.com")
recipe = dict(
    name="Recipe",
    url="http://recipe.com",
    image="http://image.com",
    ingredients="garlic tomato",
)
sid: int = None


class TestRecipe:
    @pytest.mark.asyncio
    async def test_create_source(self, event_loop, server, host, session):
        global source
        global sid
        async with session.post(f"{host}/sources/", data=dumps(source)) as resp:
            assert resp.status == 201
            response = await resp.json()
            sid = response.get("id")
            source.update({"id": sid, "url": "source.com"})
            assert response == source

    @pytest.mark.asyncio
    async def test_add_recipe(self, event_loop, server, host, session):
        global recipe
        global sid
        async with session.post(
            f"{host}/sources/{sid}/recipes/", data=dumps(recipe)
        ) as resp:
            response = await resp.json()
            recipe.update({
                "id": response.get("id"), "ingredients": {"items": ["garlic", "tomato"]}
            })
            assert resp.status == 201
            assert response == recipe

    @pytest.mark.asyncio
    async def test_get_recipe(self, event_loop, server, host, session):
        global recipe
        global sid
        async with session.get(f"{host}/sources/{sid}/recipes/{recipe['id']}/") as resp:
            assert resp.status == 200
            assert await resp.json() == recipe

    @pytest.mark.asyncio
    async def test_get_recipes(self, event_loop, server, host, session):
        global recipe
        global sid
        async with session.get(f"{host}/sources/{sid}/recipes/") as resp:
            assert resp.status == 200
            assert await resp.json() == [recipe]

    @pytest.mark.asyncio
    async def test_update_recipe(self, event_loop, server, host, session):
        global recipe
        global sid
        recipe["name"] = "Recipe 2.0"
        async with session.put(
            f"{host}/sources/{sid}/recipes/{recipe['id']}/",
            data=dumps(dict(name="Recipe 2.0")),
        ) as resp:
            assert resp.status == 200
            assert await resp.json() == recipe

    @pytest.mark.asyncio
    async def test_remove_recipe(self, event_loop, server, host, session):
        global recipe
        global sid
        async with session.delete(
            f"{host}/sources/{sid}/recipes/{recipe['id']}/"
        ) as resp:
            assert resp.status == 200
            assert await resp.json() == recipe

    @pytest.mark.asyncio
    async def test_remove_source(self, event_loop, server, host, session):
        global source
        global sid
        async with session.delete(f"{host}/sources/{sid}") as resp:
            assert resp.status == 200
            assert await resp.json() == source
