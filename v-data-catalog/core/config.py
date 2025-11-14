import logging
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent
MOVIES_STORAGE_FILEPATH = BASE_DIR / "movies.json"

LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


class RedisDbConfig(BaseModel):
    default: int = 0
    tokens: int = 1
    users: int = 2
    movies: int = 3


class RedisNameConfig(BaseModel):
    tokens_set_name: str = "tokens"
    movies_hash_name: str = "movies"


class LoggingConfig(BaseModel):
    log_level: int = logging.INFO
    log_format: str = LOG_FORMAT
    date_format: str = "%Y-%m-%d %H:%M:%S"


class RedisConnectionConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379


class RedisConfig(BaseModel):
    connection: RedisConnectionConfig = RedisConnectionConfig()
    db: RedisDbConfig = RedisDbConfig()
    names: RedisNameConfig = RedisNameConfig()


class Settings(BaseSettings):
    logging: LoggingConfig = LoggingConfig()
    redis: RedisConfig = RedisConfig()


settings = Settings()
