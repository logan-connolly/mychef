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


@pytest.mark.usefixtures("create_tables")
class TestRecipeInvalid:
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
    @pytest.mark.parametrize(
        "payload, code",
        [
            (dict(name="no url or image"), 422),
            (dict(name="Bad url", url="url", image="http://image.com"), 422),
            (dict(name="no image url", url="http://url.com", image="image"), 422),
        ],
    )
    async def test_add_recipe_invalid(self, event_loop, server, session, payload, code):
        dumps = json.dumps(payload)
        async with session.post(f"{host}/sources/1/recipes/", data=dumps) as resp:
            status = resp.status

        assert status == code

    @pytest.mark.asyncio
    async def test_get_recipe_invalid(self, event_loop, server, session):
        async with session.get(f"{host}/sources/1/recipes/999") as resp:
            status = resp.status

        assert status == 404

    @pytest.mark.asyncio
    async def test_get_recipes_invalid(self, event_loop, server, session):
        async with session.get(f"{host}/sources/999/recipes/") as resp:
            status = resp.status

        assert status == 404

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "sid, rid, payload, code",
        [
            (1, 1, {}, 422),
            (1, 1, dict(name="no url or image"), 422),
            (999, 1, dict(name="sid", url="http://u.com", image="http://i.com"), 404),
            (1, 999, dict(name="rid", url="http://u.com", image="http://i.com"), 404),
        ],
    )
    async def test_update_recipe_invalid(
        self, event_loop, server, session, sid, rid, payload, code
    ):
        dumps = json.dumps(payload)
        endpoint = f"{host}/sources/{sid}/recipes/{rid}/"
        async with session.put(endpoint, data=dumps) as resp:
            status = resp.status

        assert status == code

    @pytest.mark.asyncio
    async def test_remove_source_invalid(self, event_loop, server, session):
        async with session.delete(f"{host}/sources/1/recipes/999") as resp:
            status = resp.status

        assert status == 404
