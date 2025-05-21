import logging

from fastapi import HTTPException, BackgroundTasks
from starlette import status

from api.api_v1.video_catalog.crud import storage
from schemas.video_catalog import Movie


log = logging.getLogger(__name__)


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
    background_tasks: BackgroundTasks,
):
    # сначала код до входа внутрь view функции
    yield
    # код после покидания view функции
    log.info("Add background task to save_storage")
    background_tasks.add_task(storage.save_state)
