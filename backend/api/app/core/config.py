from pydantic import BaseSettings


class PostgresSettings(BaseSettings):
    user: str = ""
    password: str = ""
    host: str = ""
    db: str = ""

    class Config:
        env_prefix = "POSTGRES_"


class Settings(BaseSettings):
    title: str = "MyChef"
    description: str = "Recipe recommender app"
    debug: bool = False
    api_version: str = "/api/v1"
    search_url: str = "http://search:7700/indexes/recipes/documents"
    pg = PostgresSettings()
    uri: str = f"postgresql://{pg.user}:{pg.password}@{pg.host}/{pg.db}"
    async_uri: str = f"postgresql+asyncpg://{pg.user}:{pg.password}@{pg.host}/{pg.db}"


settings = Settings()
