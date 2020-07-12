import json
import pytest


ingredient = dict(ingredient="onion")


class TestIngredient:
    @pytest.mark.asyncio
    async def test_add_ingredient(self, event_loop, server, host, session):
        global ingredient
        data = json.dumps(ingredient)
        async with session.post(f"{host}/ingredients/", data=data) as resp:
            assert resp.status == 201
            response = await resp.json()
            ingredient.update({"id": response.get("id")})
            assert response == ingredient

    @pytest.mark.asyncio
    async def test_get_ingredient(self, event_loop, server, host, session):
        global ingredient
        async with session.get(f"{host}/ingredients/{ingredient.get('id')}") as resp:
            assert resp.status == 200
            assert await resp.json() == ingredient

    @pytest.mark.asyncio
    async def test_get_ingredients(self, event_loop, server, host, session):
        global ingredient
        async with session.get(f"{host}/ingredients/") as resp:
            assert resp.status == 200
            ingredients = await resp.json()
            assert ingredient in ingredients

    @pytest.mark.asyncio
    async def test_update_ingredient(self, event_loop, server, host, session):
        global ingredient
        new_ingredient = "red onion"
        ingredient["ingredient"] = new_ingredient
        data = json.dumps(dict(ingredient=new_ingredient))
        url = f"{host}/ingredients/{ingredient.get('id')}"
        async with session.put(url, data=data) as resp:
            assert resp.status == 200
            assert await resp.json() == ingredient

    @pytest.mark.asyncio
    async def test_remove_ingredient(self, event_loop, server, host, session):
        global ingredient
        async with session.delete(f"{host}/ingredients/{ingredient.get('id')}") as resp:
            assert resp.status == 200
            assert await resp.json() == ingredient
