from fastapi import HTTPException
from starlette import status

from api.api_v1.video_catalog.crud import FILM_CATALOG
from schemas.video_catalog import VideoCatalog


def read_film_id(
    id_film: int,
) -> VideoCatalog | None:
    film: VideoCatalog | None = next(
        (film for film in FILM_CATALOG if film.id_film == id_film),
        None,
    )
    if film:
        return film
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"URL{id_film!r} not found",
    )
