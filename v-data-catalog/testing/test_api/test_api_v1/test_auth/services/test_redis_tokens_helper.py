from os import getenv
from unittest import TestCase

import pytest

from api.api_v1.auth.services import redis_tokens

if getenv("TESTING") != "1":
    msg = "Environment is not ready for testing"
    pytest.exit(msg)


class RedisTokenHelperTestCase(TestCase):

    def test_generate_and_save_token(self) -> None:
        new_token = redis_tokens.generate_and_save_token()
        self.assertTrue(
            redis_tokens.token_exist(new_token),
        )
