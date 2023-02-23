from pydantic import BaseSettings


class PostgresSettings(BaseSettings):
    user: str = "mychef"
    password: str = "mychef"
    host: str = "localhost"
    db: str = "mychef_db"

    class Config:
        env_prefix = "POSTGRES_"


class MeiliSettings(BaseSettings):
    host: str = "localhost"
    port: str = "7700"

    class Config:
        env_prefix = "MEILI_"


class Settings(BaseSettings):
    title: str = "MyChef"
    description: str = "Recipe recommender app"
    debug: bool = False
    api_version: str = "/api/v1"

    meili = MeiliSettings()
    meili_url: str = f"http://{meili.host}:{meili.port}"

    pg = PostgresSettings()
    uri: str = f"postgresql://{pg.user}:{pg.password}@{pg.host}/{pg.db}"
    async_uri: str = f"postgresql+asyncpg://{pg.user}:{pg.password}@{pg.host}/{pg.db}"


settings = Settings()
