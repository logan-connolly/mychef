import json

from app.core.config import settings

ingredient = dict(ingredient="onion")
iid = None


class TestIngredient:
    def test_add_ingredient(self, client):
        global ingredient
        global iid
        data = json.dumps(ingredient)
        resp = client.post(f"{settings.API_V1_STR}/ingredients/", data=data)
        assert resp.status_code == 201
        iid = resp.json()["id"]
        ingredient.update({"id": iid})
        assert resp.json() == ingredient

    def test_get_ingredient(self, client):
        resp = client.get(f"{settings.API_V1_STR}/ingredients/{iid}/")
        assert resp.status_code == 200
        assert resp.json() == ingredient

    def test_get_ingredients(self, client):
        resp = client.get(f"{settings.API_V1_STR}/ingredients/")
        assert resp.status_code == 200
        assert ingredient in resp.json()

    def test_update_ingredient(self, client):
        global ingredient
        new_ingredient = "red onion"
        ingredient["ingredient"] = new_ingredient
        data = json.dumps(dict(ingredient=new_ingredient))
        url = f"{settings.API_V1_STR}/ingredients/{iid}/"
        resp = client.put(url, data=data)
        assert resp.status_code == 200
        assert resp.json() == ingredient

    def test_remove_ingredient(self, client):
        resp = client.delete(f"{settings.API_V1_STR}/ingredients/{iid}/")
        assert resp.status_code == 200
        assert resp.json() == ingredient
