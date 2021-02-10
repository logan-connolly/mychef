from typing import List

from pydantic import BaseSettings


class ApiSettings(BaseSettings):
    debug: bool
    model: str
    title: str = "MyChef"
    version: str = "/api/v1"

    class Config:
        env_prefix = "API_"


class PostgresSettings(BaseSettings):
    user: str
    password: str
    host: str
    db: str

    class Config:
        env_prefix = "POSTGRES_"


class WebSettings(BaseSettings):
    port: int

    class Config:
        env_prefix = "WEB_"


class SearchSettings(BaseSettings):
    host: str
    port: int

    class Config:
        env_prefix = "SEARCH_"


class Settings(BaseSettings):
    api = ApiSettings()
    web = WebSettings()
    search = SearchSettings()
    pg = PostgresSettings()

    OPENAPI_URL: str = f"{api.version}/openapi.json"
    SEARCH_URL: str = f"http://{search.host}:{search.port}"
    URI: str = f"postgres://{pg.user}:{pg.password}@{pg.host}/{pg.db}"

    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost",
        f"http://localhost:{web.port}",
    ]

    class Config:
        case_sensitive = True


settings = Settings()
api_settings = {
    "title": settings.api.title,
    "openapi_url": settings.OPENAPI_URL,
    "debug": settings.api.debug,
}
