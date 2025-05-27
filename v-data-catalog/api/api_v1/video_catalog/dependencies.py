import logging
from typing import Annotated

from fastapi import (
    HTTPException,
    BackgroundTasks,
    Request,
    Header,
)
from starlette import status

from api.api_v1.video_catalog.crud import storage
from core.config import API_TOKENS
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
        str,
        Header(alias="x-auth-token"),
    ] = "",
):
    if request.method not in UNSAFE_METHOD:
        return

    if api_token not in API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API token",
        )
