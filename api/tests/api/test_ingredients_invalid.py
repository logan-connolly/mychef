import json
import pytest


class TestIngredientInvalid:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "payload, code",
        [
            (dict(ingredient=["tomato"]), 422),
            (dict(ingredient={"name": "tomato"}), 422),
        ],
    )
    async def test_add_ingredient_invalid(
        self, event_loop, server, host, session, payload, code
    ):
        data = json.dumps(payload)
        async with session.post(f"{host}/ingredients/", data=data) as resp:
            assert resp.status == code

    @pytest.mark.asyncio
    async def test_get_ingredient_invalid(self, event_loop, host, server, session):
        async with session.get(f"{host}/ingredients/0") as resp:
            assert resp.status == 404

    @pytest.mark.asyncio
    async def test_get_ingredients_invalid(self, event_loop, host, server, session):
        async with session.get(f"{host}/ingredient/") as resp:
            assert resp.status == 404

    @pytest.mark.asyncio
    async def test_update_ingredient_invalid(self, event_loop, server, host, session):
        async with session.put(
            f"{host}/ingredients/0", data=json.dumps(dict())
        ) as resp:
            assert resp.status == 404

    @pytest.mark.asyncio
    async def test_remove_ingredient_invalid(self, event_loop, server, host, session):
        async with session.delete(f"{host}/ingredients/0") as resp:
            assert resp.status == 404
