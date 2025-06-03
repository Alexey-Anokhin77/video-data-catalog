from fastapi import (
    APIRouter,
    status,
    Depends,
)


from api.api_v1.video_catalog.crud import storage
from api.api_v1.video_catalog.dependencies import (
    save_storage_state,
    api_token_required_for_unsafe_methods,
    basic_user_auth_required_for_unsafe_methods,
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
        Depends(save_storage_state),
        # Depends(api_token_required_for_unsafe_methods),
        Depends(basic_user_auth_required_for_unsafe_methods),
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
)
def create_video(
    video_create: MovieCreate,
) -> Movie:
    return storage.create(video_create)
