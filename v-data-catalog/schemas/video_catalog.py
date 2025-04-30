from typing import Annotated

from annotated_types import Len
from pydantic import (
    BaseModel,
    Field,
)


class FilmInfoBase(BaseModel):
    slug: str
    title_film: str
    description_film: str
    time_film: float


class VideoCreate(FilmInfoBase):
    """
    Модель создания фильма
    """

    slug: Annotated[
        str,
        Len(min_length=3, max_length=100),
    ]
    title_film: Annotated[str, Field(description="Название фильма")]
    description_film: Annotated[str, Field(description="Описание фильма")]
    time_film: Annotated[float, Field(gt=0)]


class VideoCatalog(FilmInfoBase):
    """
    Модель фильма
    """
