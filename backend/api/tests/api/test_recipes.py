import json

import pytest

from app.core.config import settings

SOURCE = dict(name="Source", url="http://source.com")
RECIPE = dict(
    name="Recipe",
    url="http://recipe.com",
    image="http://image.com",
    ingredients="garlic tomato",
)
SOURCE_ID: int = None
RECIPE_ID: int = None


class TestRecipe:
    def test_create_source(self, client):
        global SOURCE_ID
        resp = client.post(f"{settings.api_version}/sources/", data=json.dumps(SOURCE))
        assert resp.status_code == 201
        SOURCE_ID = resp.json()["id"]
        SOURCE.update({"id": SOURCE_ID, "url": "source.com"})
        assert resp.json() == SOURCE

    def test_add_recipe(self, client):
        global RECIPE_ID
        data = json.dumps(RECIPE)
        resp = client.post(
            f"{settings.api_version}/sources/{SOURCE_ID}/recipes/", data=data
        )
        if resp.status_code in (404, 422):
            pytest.skip("Source cannot be found.")
        assert resp.status_code == 201
        RECIPE_ID = resp.json()["id"]
        ingredients = resp.json()["ingredients"]
        RECIPE.update({"id": RECIPE_ID, "ingredients": ingredients})
        assert resp.json() == RECIPE

    def test_get_recipe(self, client):
        resp = client.get(
            f"{settings.api_version}/sources/{SOURCE_ID}/recipes/{RECIPE_ID}/"
        )
        if resp.status_code in (404, 422):
            pytest.skip("Source cannot be found.")
        assert resp.status_code == 200
        assert resp.json() == RECIPE

    def test_get_recipes(self, client):
        resp = client.get(f"{settings.api_version}/sources/{SOURCE_ID}/recipes/")
        if resp.status_code in (404, 422):
            pytest.skip("Source cannot be found.")
        assert resp.status_code == 200

    def test_update_recipe(self, client):
        RECIPE["name"] = "Recipe 2.0"
        data = json.dumps(dict(name="Recipe 2.0"))
        resp = client.put(
            f"{settings.api_version}/sources/{SOURCE_ID}/recipes/{RECIPE_ID}/",
            data=data,
        )
        if resp.status_code in (404, 422):
            pytest.skip("Source cannot be found.")
        assert resp.status_code == 200
        assert resp.json() == RECIPE

    def test_remove_recipe(self, client):
        resp = client.delete(
            f"{settings.api_version}/sources/{SOURCE_ID}/recipes/{RECIPE_ID}/"
        )
        if resp.status_code in (404, 422):
            pytest.skip("Source cannot be found.")
        assert resp.status_code == 200
        assert resp.json() == RECIPE

    def test_remove_source(self, client):
        resp = client.delete(f"{settings.api_version}/sources/{SOURCE_ID}/")
        assert resp.status_code == 200
        assert resp.json() == SOURCE
