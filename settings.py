import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """App config"""

    APP_NAME: str = os.environ.get("APP_NAME", "silenus")
    APP_VERSION: str = os.environ.get("APP_VERSION", "0.1.0")

    LOGGER: str = "LOGGER"
