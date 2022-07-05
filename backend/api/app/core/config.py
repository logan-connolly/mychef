from pydantic import BaseSettings


class PostgresSettings(BaseSettings):
    user: str = ""
    password: str = ""
    host: str = ""
    db: str = ""

    class Config:
        env_prefix = "POSTGRES_"


class MeiliSettings(BaseSettings):
    host: str = "search"
    port: str = "7700"

    class Config:
        env_prefix = "MEILI_"


class Settings(BaseSettings):
    title: str = "MyChef"
    description: str = "Recipe recommender app"
    debug: bool = False
    api_version: str = "/api/v1"

    meili = MeiliSettings()
    search_url: str = f"http://{meili.host}:{meili.port}/indexes/recipes/documents"

    pg = PostgresSettings()
    uri: str = f"postgresql://{pg.user}:{pg.password}@{pg.host}/{pg.db}"
    async_uri: str = f"postgresql+asyncpg://{pg.user}:{pg.password}@{pg.host}/{pg.db}"


settings = Settings()
