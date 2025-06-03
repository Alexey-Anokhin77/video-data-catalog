import logging
from typing import Annotated

from fastapi import (
    HTTPException,
    BackgroundTasks,
    Request,
)
from fastapi.params import Depends

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    HTTPBasicCredentials,
    HTTPBasic,
)

from starlette import status

from api.api_v1.video_catalog.crud import storage
from core.config import API_TOKENS, USERS_DB
from schemas.video_catalog import Movie


log = logging.getLogger(__name__)

UNSAFE_METHOD = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    }
)


static_api_token = HTTPBearer(
    scheme_name="Static API token",
    description="Your **Static API token** from developer portal. [Read more](#)",
    auto_error=False,
)

user_basic_auth = HTTPBasic(
    scheme_name="Basic Auth",
    description="Basic username + password auth",
    auto_error=False,
)


def read_film_slug(
    slug: str,
) -> Movie:
    film: Movie | None = storage.get_by_slug(slug=slug)
    if film:
        return film
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Film{slug!r} not found",
    )


def save_storage_state(
    request: Request,
    background_tasks: BackgroundTasks,
):
    # сначала код до входа внутрь view функции
    yield
    # код после покидания view функции
    if request.method in UNSAFE_METHOD:
        log.info("Add background task to save_storage")
        background_tasks.add_task(storage.save_state)


def api_token_required_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
):
    log.info("Api token: %s", api_token)

    if request.method not in UNSAFE_METHOD:
        return

    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API token is required",
        )

    if api_token.credentials not in API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API token",
        )


def basic_user_auth_required_for_unsafe_methods(
    request: Request,
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
    ] = None,
):
    log.info("Users auth credentials: %s", credentials)

    if request.method not in UNSAFE_METHOD:
        return

    if (
        credentials
        and credentials.username in USERS_DB
        and USERS_DB[credentials.username] == credentials.password
    ):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User credentials required. Incorrect username or password.",
        headers={"WWW-Authenticate": "Basic"},
    )
