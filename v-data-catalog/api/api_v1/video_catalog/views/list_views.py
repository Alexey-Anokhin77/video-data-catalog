from fastapi import (
    APIRouter,
    status,
    BackgroundTasks,
)


from api.api_v1.video_catalog.crud import storage

from schemas.video_catalog import (
    Movie,
    MovieCreate,
    MovieRead,
)

router = APIRouter(
    prefix="/film-catalog",
    tags=["Film catalog"],
)


@router.get(
    "/",
    response_model=list[MovieRead],
)
def read_film_catalog_list() -> list[Movie]:
    return storage.get()


@router.post(
    "/",
    response_model=MovieRead,
    status_code=status.HTTP_201_CREATED,
)
def create_video(
    video_create: MovieCreate,
    background_tasks: BackgroundTasks,
) -> Movie:
    background_tasks.add_task(storage.save_state)
    return storage.create(video_create)
