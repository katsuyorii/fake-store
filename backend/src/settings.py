from pydantic import EmailStr
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

class JWTSettings(CustomBaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

class RedisSettings(CustomBaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_POOL_SIZE: int

class RabbitMQSettings(CustomBaseSettings):
    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASS: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int

    @property
    def RABBIT_MQ_URL(self) -> str:
        return f"amqp://{self.RABBITMQ_DEFAULT_USER}:{self.RABBITMQ_DEFAULT_PASS}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}//"

class SMTPSettings(CustomBaseSettings):
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: EmailStr
    SMTP_PASSWORD: str
    EMAIL_MESSAGE_EXPIRE_MINUTES: int

class PATHSettings(CustomBaseSettings):
    BASE_URL: str
    EMAIL_VERIFY_PATH: str
    EMAIL_CHANGE_PATH: str

database_settings = DatabaseSettings()
jwt_settings = JWTSettings()
redis_settings = RedisSettings()
rabbit_mq_settings = RabbitMQSettings()
smtp_settings = SMTPSettings()
path_settings = PATHSettings()