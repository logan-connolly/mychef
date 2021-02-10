from typing import List

from pydantic import BaseSettings


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
    DEBUG: int = 1
    API_MODEL: str = ""

    API_TITLE: str = "MyChef"
    API_V1_STR: str = "/api/v1"
    OPENAPI_URL: str = f"{API_V1_STR}/openapi.json"

    WEB = WebSettings()
    SEARCH = SearchSettings()
    PG = PostgresSettings()

    SEARCH_URL: str = f"http://{SEARCH.host}:{SEARCH.port}"
    URI: str = f"postgres://{PG.user}:{PG.password}@{PG.host}/{PG.db}"

    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost",
        f"http://localhost:{WEB.port}",
    ]

    class Config:
        case_sensitive = True


settings = Settings()
api_settings = {
    "title": settings.API_TITLE,
    "openapi_url": settings.OPENAPI_URL,
    "debug": settings.DEBUG,
}
