from fastapi import APIRouter

from .video_catalog.views import router as video_catalog_router

router = APIRouter(
    prefix="/v1",
)

router.include_router(video_catalog_router)
