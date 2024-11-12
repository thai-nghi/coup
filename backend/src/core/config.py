from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    POSTGRES_HOST: str = "127.0.0.1"
    DB_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRES_MINUTES: int = 500
    REFRESH_TOKEN_EXPIRES_MINUTES: int = 15 * 24 * 60  # 15 days

    SECRET_KEY: str

    GAME_SERVER_ACCESS: str

    QUERY_CACHE_SIZE: int = 1200

    class Config:
        env_file = '.dev.env'
        env_file_encoding = 'utf-8'


class DevSettings(Settings):
    
    class Config:
        env_file = '.dev.env'
        env_file_encoding = 'utf-8'


class TestSettings(Settings):
    QUERY_CACHE_SIZE: int = 0
    class Config:
        env_file = '.test.env'
        env_file_encoding = 'utf-8'

current_env = os.getenv("ENV", "dev")

if current_env == "dev":
    settings = DevSettings()
elif current_env == "test":
    settings = TestSettings()
else:
    settings = Settings()
