from pydantic import BaseSettings


class PostgresSettings(BaseSettings):
    user: str = ""
    password: str = ""
    host: str = ""
    db: str = ""

    class Config:
        env_prefix = "POSTGRES_"


class Settings(BaseSettings):
    ingredient_model: str = "v1"
    debug: bool = False
    api_version: str = "/api/v1"
    search_url: str = "http://search:7700/indexes/recipes/documents"
    pg = PostgresSettings()
    uri: str = f"postgresql://{pg.user}:{pg.password}@{pg.host}/{pg.db}"


settings = Settings()
