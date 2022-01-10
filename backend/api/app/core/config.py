from typing import List

from pydantic import BaseSettings


class ApiSettings(BaseSettings):
    ingredient_model: str = "v1"
    debug: bool = False
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


class Settings(BaseSettings):
    api = ApiSettings()
    pg = PostgresSettings()

    OPENAPI_URL: str = f"{api.version}/openapi.json"
    SEARCH_URL: str = "http://search:7700/indexes/recipes/documents"
    URI: str = f"postgresql://{pg.user}:{pg.password}@{pg.host}/{pg.db}"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost"]

    class Config:
        case_sensitive = True


settings = Settings()
api_settings = {
    "title": settings.api.title,
    "openapi_url": settings.OPENAPI_URL,
    "debug": settings.api.debug,
}
