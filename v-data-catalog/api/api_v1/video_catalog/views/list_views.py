from fastapi import (
    APIRouter,
    status,
)

from api.api_v1.video_catalog.crud import storage

from schemas.video_catalog import VideoCatalog, VideoCreate

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
