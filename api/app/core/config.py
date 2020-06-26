from pydantic import BaseSettings, PostgresDsn


class PostgresSettings(BaseSettings):
    user: str
    password: str
    host: str
    db: str

    class Config:
        env_prefix = "POSTGRES_"


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"

    PG = PostgresSettings()
    URI: PostgresDsn = f"postgres://{PG.user}:{PG.password}@{PG.host}/{PG.db}"

    class Config:
        case_sensitive = True


settings = Settings()
