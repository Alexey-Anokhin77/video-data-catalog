import logging
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent
MOVIES_STORAGE_FILEPATH = BASE_DIR / "movies.json"

LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

REDIS_DB = 0
REDIS_DB_TOKENS = 1
REDIS_DB_USERS = 2
REDIS_DB_MOVIES = 3


REDIS_TOKENS_SET_NAME = "tokens"
REDIS_MOVIES_HASH_NAME = "movies"


class LoggingConfig(BaseModel):
    log_level: int = logging.INFO
    log_format: str = LOG_FORMAT
    date_format: str = "%Y-%m-%d %H:%M:%S"


class RedisConnectionConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379


class RedisConfig(BaseModel):
    connection: RedisConnectionConfig = RedisConnectionConfig()


class Settings(BaseSettings):
    logging: LoggingConfig = LoggingConfig()
    redis: RedisConfig = RedisConfig()


settings = Settings()
