from pydantic import BaseSettings, PostgresDsn, SecretStr


class PostgresSettings(BaseSettings):
    user: str
    password: SecretStr
    host: str
    db: str

    class Config:
        env_prefix = "postgres_"


class Settings(BaseSettings):

    pg = PostgresSettings()
    base_db_url: PostgresDsn = (
        f"postgresql://{pg.user}:{pg.password.get_secret_value()}@{pg.host}"
    )
    db_url: PostgresDsn = base_db_url + f"/{pg.db}"
    test_db_url: PostgresDsn = base_db_url + f"/{pg.db}_test"

    testing: bool = False


settings = Settings()
