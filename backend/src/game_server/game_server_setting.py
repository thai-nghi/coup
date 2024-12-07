import os

from pydantic_settings import BaseSettings


class GameServerSettings(BaseSettings):

    API_HOST: str = "http://192.168.31.115:8001/webhooks"
    SECRET_KEY: str

    GAME_SERVER_ACCESS: str

    QUERY_CACHE_SIZE: int = 1200

    class Config:
        env_file = ".dev.env"
        env_file_encoding = "utf-8"
        extra = "allow"


GAME_SERVER_SETTINGS = GameServerSettings()
