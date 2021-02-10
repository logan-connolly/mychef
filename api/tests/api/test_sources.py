import json

from app.core.config import settings

source = dict(name="Example", url="http://example.com")
sid = None


class TestSource:
    def test_add_source(self, client):
        global source
        global sid
        resp = client.post(f"{settings.api.version}/sources/", data=json.dumps(source))
        assert resp.status_code == 201
        sid = resp.json()["id"]
        source.update({"id": sid, "url": "example.com"})
        assert resp.json() == source

    def test_get_source(self, client):
        resp = client.get(f"{settings.api.version}/sources/{sid}/")
        assert resp.status_code == 200
        assert resp.json() == source

    def test_get_sources(self, client):
        resp = client.get(f"{settings.api.version}/sources/")
        assert resp.status_code == 200
        assert source in resp.json()

    def test_update_source(self, client):
        new_url = "http://newexample.com"
        source["url"] = new_url
        payload = json.dumps(dict(url=new_url))
        resp = client.put(f"{settings.api.version}/sources/{sid}/", data=payload)
        assert resp.status_code == 200
        assert resp.json() == source

    def test_remove_source(self, client):
        resp = client.delete(f"{settings.api.version}/sources/{sid}/")
        assert resp.status_code == 200
        assert resp.json() == source
