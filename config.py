from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote_plus

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def database_url_async(self) -> str:
        user = quote_plus(self.DB_USER)
        password = quote_plus(self.DB_PASS)
        return f"postgresql+asyncpg://{user}:{password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def database_url_psycopg(self) -> str:
        user = quote_plus(self.DB_USER)
        password = quote_plus(self.DB_PASS)
        return f"postgresql://{user}:{password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()