from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from api.api_v1.video_catalog.crud import storage
from api.api_v1.video_catalog.dependencies import read_film_slug
from schemas.video_catalog import (
    Movie,
    MovieUpdate,
)

router = APIRouter(
    prefix="/{slug}",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Film not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Film 'slug' not found",
                    },
                },
            },
        },
    },
)

Movie_BY_Slug = Annotated[
    Movie,
    Depends(read_film_slug),
]


@router.get(
    "/",
    response_model=Movie,
    summary="Получить фильм по Slug",
)
def read_film_details(
    film: Movie_BY_Slug,
) -> Movie:
    return film


@router.put(
    "/",
    response_model=Movie,
)
def update_movie_details(
    film: Movie_BY_Slug,
    film_in: MovieUpdate,
):
    return storage.update(
        movie=film,
        film_in=film_in,
    )


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_film(
    film: Movie_BY_Slug,
) -> None:
    storage.delete(film=film)
