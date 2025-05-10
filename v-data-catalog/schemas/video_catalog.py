from typing import Annotated

from annotated_types import (
    Len,
    MaxLen,
)
from pydantic import (
    BaseModel,
)


class FilmInfoBase(BaseModel):
    time_film: float
    title_film: str
    description_film: Annotated[
        str,
        MaxLen(1000),
    ] = ""


class MovieCreate(FilmInfoBase):
    """
    Модель создания фильма
    """

    slug: Annotated[
        str,
        Len(min_length=3, max_length=100),
    ]


class MovieUpdate(FilmInfoBase):
    """
    Модель для обновления информации о фильме.
    """

    time_film: float
    title_film: str
    description_film: Annotated[
        str,
        MaxLen(1000),
    ]


class Movie(FilmInfoBase):
    """
    Модель фильма
    """

    slug: str
