from fastapi import (
    APIRouter,
    status,
    Depends,
    HTTPException,
)


from api.api_v1.video_catalog.crud import (
    storage,
    MovieAlreadyExistsError,
)
from api.api_v1.video_catalog.dependencies import (
    api_token_or_basic_auth_required_for_unsafe_methods,
)

from schemas.video_catalog import (
    Movie,
    MovieCreate,
    MovieRead,
)

router = APIRouter(
    prefix="/film-catalog",
    tags=["Film catalog"],
    dependencies=[
        Depends(api_token_or_basic_auth_required_for_unsafe_methods),
    ],
    responses={
        # status.HTTP_204_NO_CONTENT: None,
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthenticated. Only for unsafe methods.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid API token",
                    },
                },
            },
        },
    },
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
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "Conflict. Movie with this slug already exists.",
            "content": {
                "application/json": {
                    "example": {"detail": "Movie with slug='example' already exists"},
                },
            },
        },
    },
)
def create_video(
    video_create: MovieCreate,
) -> Movie:
    try:
        return storage.create_or_raise_if_exists(video_create)
    except MovieAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Movie with slug={video_create.slug!r} already exist",
        )
