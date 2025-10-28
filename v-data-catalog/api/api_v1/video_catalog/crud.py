__all__ = (
    "MovieAlreadyExistsError",
    "storage",
)

import logging
from typing import cast, Iterable

from pydantic import BaseModel
from redis import Redis

from core import config
from schemas.video_catalog import (
    Movie,
    MovieCreate,
    MoviePartialUpdate,
    MovieUpdate,
)

log = logging.getLogger(__name__)

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_MOVIES,
    decode_responses=True,
)


class MovieBaseError(Exception):
    """
    Base exception for movie CRUD actions.
    """


class MovieAlreadyExistsError(MovieBaseError):
    """
    Raised on movie creation if such slug already exists.
    """


class VideoStorage(BaseModel):

    def save_movie(self, movie: Movie) -> None:
        redis.hset(
            name=config.REDIS_MOVIES_HASH_NAME,
            key=movie.slug,
            value=movie.model_dump_json(),
        )

    # Получение списка
    def get(self) -> list[Movie]:
        return [
            Movie.model_validate_json(value)
            for value in cast(
                Iterable[str], redis.hvals(name=config.REDIS_MOVIES_HASH_NAME)
            )
        ]

    # Получение по slug
    def get_by_slug(self, slug: str) -> Movie | None:
        if movies_data := redis.hget(
            name=config.REDIS_MOVIES_HASH_NAME,
            key=slug,
        ):
            return Movie.model_validate_json(movies_data)
        return None

    # Создание нового видео
    def create(self, video_in: MovieCreate) -> Movie:
        movie = Movie(
            **video_in.model_dump(),
        )
        self.save_movie(movie)
        log.info("Movie successfully created %s", movie)
        return movie

    def exists(self, slug: str) -> bool:
        return redis.hexists(
            name=config.REDIS_MOVIES_HASH_NAME,
            key=slug,
        )

    def create_or_raise_if_exists(self, video_in: MovieCreate) -> Movie:
        if not self.exists(video_in.slug):
            return self.create(video_in)

        log.info("Movie can not be created!")
        raise MovieAlreadyExistsError(video_in.slug)

    def delete_by_slug(self, slug: str) -> None:
        """Удаляет фильм по slug. Не возвращает статус операции."""
        redis.hdel(config.REDIS_MOVIES_HASH_NAME, slug)

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(slug=movie.slug)

    def update(
        self,
        movie: Movie,
        movie_in: MovieUpdate,
    ) -> Movie:  # Получаем словарь с данными
        update_data = movie_in.model_dump()
        # Обновляем поля
        for field_name, value in update_data.items():
            setattr(movie, field_name, value)
        self.save_movie(movie)

        return movie

    def partial_update(
        self,
        movie: Movie,
        movie_in: MoviePartialUpdate,
    ) -> Movie:
        # Получаем только переданные поля
        update_data = movie_in.model_dump(exclude_unset=True)
        # Обновляем только указанные поля
        for field_name, value in update_data.items():
            setattr(movie, field_name, value)
        self.save_movie(movie)
        return movie


storage = VideoStorage()
