from typing import Annotated

from annotated_types import (
    Len,
    MaxLen,
    Ge,
    Le,
)
from pydantic import (
    BaseModel,
)

DescriptionString = Annotated[
    str,
    MaxLen(1000),
]


class FilmInfoBase(BaseModel):
    time_film: float
    title_film: str
    description_film: DescriptionString = ""
    genre: Annotated[str, MaxLen(50)]
    production_year: Annotated[int, Ge(1900), Le(2100)]


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

    description_film: DescriptionString


class MoviePartialUpdate(BaseModel):
    """
    Модель для частичного обновления информации о фильме.
    """

    title_film: str | None = None
    time_film: float | None = None
    description_film: DescriptionString | None = None
    genre: Annotated[str, MaxLen(50)] | None = None
    production_year: Annotated[int, Ge(1900), Le(2100)] | None = None


class MovieRead(FilmInfoBase):
    """
    Модель для чтения данных о фильме.
    """

    slug: str


class Movie(FilmInfoBase):
    """
    Модель фильма
    """

    slug: str
    notes: str
