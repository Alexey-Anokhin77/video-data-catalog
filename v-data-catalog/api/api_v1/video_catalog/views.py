from fastapi import (
    APIRouter,
    Depends,
    status,
)
from typing import Annotated

from api.api_v1.video_catalog.crud import storage

from schemas.video_catalog import VideoCatalog, VideoCreate
from .dependencies import read_film_slug

router = APIRouter(
    prefix="/film-catalog",
    tags=["Film catalog"],
)


@router.get(
    "/",
    response_model=list[VideoCatalog],
)
def read_film_catalog_list() -> list[VideoCatalog]:
    return storage.get()


@router.post(
    "/",
    response_model=VideoCatalog,
    status_code=status.HTTP_201_CREATED,
)
def create_video(
    video_create: VideoCreate,
) -> VideoCatalog:
    return storage.create(video_create)


@router.get(
    "/{slug}/",
    response_model=VideoCatalog,
    summary="Получить фильм по Slug",
)
def read_film_details(
    film: Annotated[
        VideoCatalog,
        Depends(read_film_slug),
    ],
) -> VideoCatalog:
    return film


@router.delete(
    "/{slug}/",
    status_code=status.HTTP_204_NO_CONTENT,
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
def delete_film(
    film: Annotated[
        VideoCatalog,
        Depends(read_film_slug),
    ],
) -> None:
    storage.delete(film=film)
