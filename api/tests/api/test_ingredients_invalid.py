import json
import pytest

from app.core.config import settings


class TestIngredientInvalid:
    @pytest.mark.parametrize(
        "payload, code",
        [
            (dict(ingredient=["tomato"]), 422),
            (dict(ingredient={"name": "tomato"}), 422),
        ],
    )
    def test_add_ingredient_invalid(self, client, payload, code):
        data = json.dumps(payload)
        resp = client.post(f"{settings.api.version}/ingredients/", data=data)
        assert resp.status_code == code

    def test_get_ingredient_invalid(self, client):
        resp = client.get(f"{settings.api.version}/ingredients/0/")
        assert resp.status_code == 404

    def test_get_ingredients_invalid(self, client):
        resp = client.get(f"{settings.api.version}/ingredient/")
        assert resp.status_code == 404

    def test_update_ingredient_invalid(self, client):
        resp = client.put(
            f"{settings.api.version}/ingredients/0/", data=json.dumps(dict())
        )
        assert resp.status_code == 404

    def test_remove_ingredient_invalid(self, client):
        resp = client.delete(f"{settings.api.version}/ingredients/0/")
        assert resp.status_code == 404
