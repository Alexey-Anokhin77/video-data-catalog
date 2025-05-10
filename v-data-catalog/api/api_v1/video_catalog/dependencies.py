from fastapi import HTTPException
from starlette import status

from api.api_v1.video_catalog.crud import storage
from schemas.video_catalog import Movie


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
