from redis import Redis

from api.api_v1.auth.services.tokens_helper import AbstractTokensHelper
from core import config
from core.config import settings


class RedisTokenHelper(AbstractTokensHelper):
    def __init__(
        self,
        host: str,
        port: int,
        db: int,
        tokens_set_name: str,
    ) -> None:
        self.redis = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
        )
        self.tokens_set = tokens_set_name

    def token_exist(self, token: str) -> bool:
        return bool(
            self.redis.sismember(
                self.tokens_set,
                token,
            ),
        )

    def add_token(self, token: str) -> None:
        self.redis.sadd(self.tokens_set, token)

    def get_tokens(self) -> list[str]:
        tokens = self.redis.smembers(self.tokens_set)

        if isinstance(tokens, set):
            return list(tokens)
        msg = "Async Redis client used in sync context or cache trouble"
        raise RuntimeError(
            msg,
        )

    def delete_token(self, token: str) -> None:
        self.redis.srem(self.tokens_set, token)


redis_tokens = RedisTokenHelper(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=config.REDIS_DB_TOKENS,
    tokens_set_name=config.REDIS_TOKENS_SET_NAME,
)
