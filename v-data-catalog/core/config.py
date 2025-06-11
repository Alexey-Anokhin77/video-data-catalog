import logging

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MOVIES_STORAGE_FILEPATH = BASE_DIR / "movies.json"


LOG_LEVEL = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

# Never store real tokens here!
# Only fake values
API_TOKENS: frozenset[str] = frozenset(
    {
        "Kn6VbFKNiVoLsCLLGJrVpg",
        "cuL_J6SAENR79FGGlxy_yA",
        "SKNsdZnA7TfLskX85TvZNg",
    }
)

# Only for demo!
# no real users in code !!!
USERS_DB: dict[str, str] = {
    # username: password
    "max": "password",
    "kix": "qwerty",
}

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
