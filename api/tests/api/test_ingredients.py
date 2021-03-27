import json

from app.core.config import settings

INGRED = dict(ingredient="onion")
INGRED_ID = None


class TestIngredient:
    def test_add_ingredient(self, client):
        global INGRED_ID
        data = json.dumps(INGRED)
        resp = client.post(f"{settings.api.version}/ingredients/", data=data)
        assert resp.status_code == 201
        INGRED_ID = resp.json()["id"]
        INGRED.update({"id": INGRED_ID})
        assert resp.json() == INGRED

    def test_get_ingredient(self, client):
        resp = client.get(f"{settings.api.version}/ingredients/{INGRED_ID}/")
        assert resp.status_code == 200
        assert resp.json() == INGRED

    def test_get_ingredients(self, client):
        resp = client.get(f"{settings.api.version}/ingredients/")
        assert resp.status_code == 200
        assert INGRED in resp.json()

    def test_update_ingredient(self, client):
        new_ingredient = "red onion"
        INGRED["ingredient"] = new_ingredient
        data = json.dumps(dict(ingredient=new_ingredient))
        url = f"{settings.api.version}/ingredients/{INGRED_ID}/"
        resp = client.put(url, data=data)
        assert resp.status_code == 200
        assert resp.json() == INGRED

    def test_remove_ingredient(self, client):
        resp = client.delete(f"{settings.api.version}/ingredients/{INGRED_ID}/")
        assert resp.status_code == 200
        assert resp.json() == INGRED
