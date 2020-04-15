import json

import pytest


host = "http://127.0.0.1:5000"


@pytest.mark.usefixtures("create_tables")
class TestRecipe:
    @pytest.mark.asyncio
    async def test_create_source(self, event_loop, server, session):
        payload = dict(name="Example", url="http://example.com")
        dumps = json.dumps(payload)
        async with session.post(f"{host}/sources/", data=dumps) as resp:
            data = await resp.json()

        assert data["id"] == 1

    @pytest.mark.asyncio
    async def test_add_recipe(self, event_loop, server, session):
        payload = dict(name="Recipe", url="http://recipe.com", image="http://image.com")
        dumps = json.dumps(payload)

        async with session.post(f"{host}/sources/1/recipes/", data=dumps) as resp:
            data = await resp.json()
            status = resp.status

        assert status == 201
        assert data == dict(
            id=1, name="Recipe", url="http://recipe.com", image="http://image.com"
        )

    @pytest.mark.asyncio
    async def test_get_recipe(self, event_loop, server, session):
        expected = dict(
            id=1, name="Recipe", url="http://recipe.com", image="http://image.com"
        )

        async with session.get(f"{host}/sources/1/recipes/1/") as resp:
            data = await resp.json()
            status = resp.status

        assert status == 200
        assert data == expected

    @pytest.mark.asyncio
    async def test_get_recipes(self, event_loop, server, session):
        expected = [
            {
                "id": 1,
                "name": "Recipe",
                "url": "http://recipe.com",
                "image": "http://image.com",
            }
        ]

        async with session.get(f"{host}/sources/1/recipes/") as resp:
            data = await resp.json()
            status = resp.status

        assert status == 200
        assert data == expected

    @pytest.mark.asyncio
    async def test_update_recipe(self, event_loop, server, session):
        payload = dict(name="New", url="http://new.com", image="http://image.com")
        dumps = json.dumps(payload)

        async with session.put(f"{host}/sources/1/recipes/1/", data=dumps) as resp:
            data = await resp.json()
            status = resp.status

        assert status == 200
        payload.update({"id": 1})
        assert data == payload

    @pytest.mark.asyncio
    async def test_remove_recipe(self, event_loop, server, session):
        expected = dict(
            id=1, name="New", url="http://new.com", image="http://image.com"
        )

        async with session.delete(f"{host}/sources/1/recipes/1/") as resp:
            data = await resp.json()
            status = resp.status

        assert status == 200
        assert data == expected
