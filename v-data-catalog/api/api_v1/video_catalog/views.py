from fastapi import APIRouter, Depends
from typing import Annotated
from api.api_v1.video_catalog.crud import FILM_CATALOG

from schemas.video_catalog import VideoCatalog
from .dependencies import read_film_id

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


@router.get(
    "/{title_film}/",
    response_model=VideoCatalog,
)
def read_film_details(
    url: Annotated[
        VideoCatalog,
        Depends(read_film_id),
    ],
) -> VideoCatalog:
    return url
