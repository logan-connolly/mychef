import pytest
import falcon
import msgpack

from falcon import testing

from mychef_scraper.app import api


@pytest.mark.usefixtures("doc")
class TestSources:
    @pytest.fixture(scope="class")
    def client(self):
        yield testing.TestClient(api)

    def test_list_sources(self, client):
        response = client.simulate_get('/sources')
        assert response.status == falcon.HTTP_OK

    def test_get_source(self, client, doc):
        sid = 1
        response = client.simulate_get(f'/source/{sid}')
        result_doc = msgpack.unpackb(response.content, raw=False)
        assert result_doc == {"source": doc["sources"][0]}
        assert response.status == falcon.HTTP_OK

    def test_get_source_not_found(self, client, doc):
        sid = -1
        response = client.simulate_get(f'/source/{sid}')
        result_doc = msgpack.unpackb(response.content, raw=False)
        assert result_doc == {"message": "Source not found."}
        assert response.status == falcon.HTTP_OK
