from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)
from starlette import status

from api.api_v1.video_catalog.crud import storage
from api.api_v1.video_catalog.dependencies import read_film_slug
from schemas.video_catalog import (
    Movie,
    MovieUpdate,
    MoviePartialUpdate,
    MovieRead,
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

MovieBySlug = Annotated[
    Movie,
    Depends(read_film_slug),
]


@router.get(
    "/",
    response_model=MovieRead,
    summary="Получить фильм по Slug",
)
def read_film_details(
    film: MovieBySlug,
) -> Movie:
    return film


@router.put(
    "/",
    response_model=MovieRead,
)
def update_movie_details(
    film: MovieBySlug,
    movie_in: MovieUpdate,
) -> Movie:
    return storage.update(
        movie=film,
        movie_in=movie_in,
    )


@router.patch(
    "/",
    response_model=MovieRead,
)
def update_movie_details_partial(
    movie: MovieBySlug,
    movie_in: MoviePartialUpdate,
) -> Movie:
    return storage.partial_update(
        movie=movie,
        movie_in=movie_in,
    )


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_film(
    movie: MovieBySlug,
) -> None:
    storage.delete(movie=movie)
