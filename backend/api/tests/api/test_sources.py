import json

from app.core.config import settings

SOURCE = dict(name="Example", url="http://example.com")
SOURCE_ID = None


class TestSource:
    def test_add_source(self, client):
        global SOURCE_ID
        resp = client.post(f"{settings.api.version}/sources/", data=json.dumps(SOURCE))
        assert resp.status_code == 201
        SOURCE_ID = resp.json()["id"]
        SOURCE.update({"id": SOURCE_ID, "url": "example.com"})
        assert resp.json() == SOURCE

    def test_get_source(self, client):
        resp = client.get(f"{settings.api.version}/sources/{SOURCE_ID}/")
        assert resp.status_code == 200
        assert resp.json() == SOURCE

    def test_get_sources(self, client):
        resp = client.get(f"{settings.api.version}/sources/")
        assert resp.status_code == 200
        assert SOURCE in resp.json()

    def test_update_source(self, client):
        new_url = "http://newexample.com"
        SOURCE["url"] = new_url
        payload = json.dumps(dict(url=new_url))
        resp = client.put(f"{settings.api.version}/sources/{SOURCE_ID}/", data=payload)
        assert resp.status_code == 200
        assert resp.json() == SOURCE

    def test_remove_source(self, client):
        resp = client.delete(f"{settings.api.version}/sources/{SOURCE_ID}/")
        assert resp.status_code == 200
        assert resp.json() == SOURCE
