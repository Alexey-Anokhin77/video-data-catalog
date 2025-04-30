from fastapi import (
    APIRouter,
    Depends,
    status,
)
from typing import Annotated
import random

from api.api_v1.video_catalog.crud import FILM_CATALOG

from schemas.video_catalog import VideoCatalog, VideoCreate
from .dependencies import read_film_slug

router = APIRouter(
    prefix="/video-catalog",
    tags=["Film catalog"],
)


@router.get(
    "/",
    response_model=list[VideoCatalog],
)
def read_film_catalog_list():
    return FILM_CATALOG


@router.post(
    "/",
    response_model=VideoCatalog,
    status_code=status.HTTP_201_CREATED,
)
def create_video(
    video_create: VideoCreate,
):
    return VideoCatalog(
        **video_create.model_dump(),
    )


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
