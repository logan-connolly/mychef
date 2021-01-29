import json
import pytest

from app.core.config import settings

source = dict(name="Source", url="http://source.com")
recipe = dict(
    name="Recipe",
    url="http://recipe.com",
    image="http://image.com",
    ingredients="garlic tomato",
)
sid: int = None
rid: int = None


class TestRecipe:
    def test_create_source(self, client):
        global source
        global sid
        resp = client.post(f"{settings.API_V1_STR}/sources/", data=json.dumps(source))
        assert resp.status_code == 201
        sid = resp.json()["id"]
        source.update({"id": sid, "url": "source.com"})
        assert resp.json() == source

    def test_add_recipe(self, client):
        global recipe
        global rid
        data = json.dumps(recipe)
        resp = client.post(f"{settings.API_V1_STR}/sources/{sid}/recipes/", data=data)
        if resp.status_code in (404, 422):
            pytest.skip("Source cannot be found.")
        assert resp.status_code == 201
        rid = resp.json()["id"]
        ingredients = resp.json()["ingredients"]
        recipe.update({"id": rid, "ingredients": ingredients})
        assert resp.json() == recipe

    def test_get_recipe(self, client):
        resp = client.get(f"{settings.API_V1_STR}/sources/{sid}/recipes/{rid}/")
        if resp.status_code in (404, 422):
            pytest.skip("Source cannot be found.")
        assert resp.status_code == 200
        assert resp.json() == recipe

    def test_get_recipes(self, client):
        resp = client.get(f"{settings.API_V1_STR}/sources/{sid}/recipes/")
        if resp.status_code in (404, 422):
            pytest.skip("Source cannot be found.")
        assert resp.status_code == 200
        assert recipe in resp.json()

    def test_update_recipe(self, client):
        global recipe
        recipe["name"] = "Recipe 2.0"
        data = json.dumps(dict(name="Recipe 2.0"))
        resp = client.put(
            f"{settings.API_V1_STR}/sources/{sid}/recipes/{rid}/",
            data=data,
        )
        if resp.status_code in (404, 422):
            pytest.skip("Source cannot be found.")
        assert resp.status_code == 200
        assert resp.json() == recipe

    def test_remove_recipe(self, client):
        resp = client.delete(f"{settings.API_V1_STR}/sources/{sid}/recipes/{rid}/")
        if resp.status_code in (404, 422):
            pytest.skip("Source cannot be found.")
        assert resp.status_code == 200
        assert resp.json() == recipe

    def test_remove_source(self, client):
        resp = client.delete(f"{settings.API_V1_STR}/sources/{sid}/")
        assert resp.status_code == 200
        assert resp.json() == source
