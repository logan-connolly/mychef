from typing import List

from pydantic import BaseSettings, PostgresDsn, AnyHttpUrl


class PostgresSettings(BaseSettings):
    user: str
    password: str
    host: str
    db: str

    class Config:
        env_prefix = "POSTGRES_"


class Settings(BaseSettings):
    DEBUG: bool = True

    API_TITLE: str = "MyChef"
    API_V1_STR: str = "/api/v1"
    OPENAPI_URL: str = f"{API_V1_STR}/openapi.json"

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost",
        "http://localhost:8080",
    ]

    MODEL: str = ""

    PG = PostgresSettings()
    URI: PostgresDsn = f"postgres://{PG.user}:{PG.password}@{PG.host}/{PG.db}"

    class Config:
        case_sensitive = True


settings = Settings()


api_settings = {
    "title": settings.API_TITLE,
    "openapi_url": settings.OPENAPI_URL,
    "debug": settings.DEBUG,
}
