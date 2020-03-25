from app.api.sources import CRUD


def test_list_sources(test_app, monkeypatch):
    test_data = [
        {"id": 1, "name": "Site 1", "url": "http://site_one.com"},
        {"id": 2, "name": "Site 2", "url": "http://site_two.com"},
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(CRUD, "get_all", mock_get_all)

    response = test_app.get("/sources/")
    assert response.status_code == 200
    assert response.json() == test_data
