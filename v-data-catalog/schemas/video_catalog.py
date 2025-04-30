import random
from typing import Annotated

from pydantic import (
    BaseModel,
    Field,
)


class FilmInfoBase(BaseModel):
    title_film: str
    description_film: str
    time_film: float


class VideoCreate(FilmInfoBase):
    """
    Модель создания фильма
    """

    title_film: Annotated[str, Field(description="Название фильма")]
    description_film: Annotated[str, Field(description="Описание фильма")]
    time_film: Annotated[float, Field(gt=0)]


class VideoCatalog(FilmInfoBase):
    """
    Модель фильма
    """

    id_film: int = Field(
        default_factory=lambda: random.randint(1, 10000),
        description="Автоматически генерируемый ID",
    )
