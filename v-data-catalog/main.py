import logging

from fastapi import (
    FastAPI,
)

from api import router as api_router
from api.main_views import router as main_router
from app_lifespan import lifespan
from core import config

logging.basicConfig(
    level=config.LOG_LEVEL,
    format=config.LOG_FORMAT,
)
app = FastAPI(
    title="Films Data Catalog",
    lifespan=lifespan,
)

app.include_router(api_router)
app.include_router(main_router)
