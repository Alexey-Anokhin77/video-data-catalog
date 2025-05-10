from fastapi import (
    APIRouter,
    status,
)

from api.api_v1.video_catalog.crud import storage

from schemas.video_catalog import Movie, MovieCreate

router = APIRouter(
    prefix="/film-catalog",
    tags=["Film catalog"],
)


@router.get(
    "/",
    response_model=list[Movie],
)
def read_film_catalog_list() -> list[Movie]:
    return storage.get()


@router.post(
    "/",
    response_model=Movie,
    status_code=status.HTTP_201_CREATED,
)
def create_video(
    video_create: MovieCreate,
) -> Movie:
    return storage.create(video_create)
