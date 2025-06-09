from pydantic_settings import BaseSettings, SettingsConfigDict


class CustomBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='../.env', extra='allow')

class DatabaseSettings(CustomBaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    @property
    def DATABASE_URL(self) -> str:
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

database_settings = DatabaseSettings()