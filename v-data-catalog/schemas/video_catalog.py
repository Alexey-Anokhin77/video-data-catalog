from pydantic import BaseModel


class FilmInfoBase(BaseModel):
    id_film: int
    title_film: str
    description_film: str
    time_film: float


class VideoCatalog(FilmInfoBase):
    """
    Модель сокращенной ссылки
    """
