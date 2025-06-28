import logging

from pydantic import BaseModel, ValidationError
from redis import Redis

from core import config
from core.config import MOVIES_STORAGE_FILEPATH
from schemas.video_catalog import (
    Movie,
    MovieCreate,
    MovieUpdate,
    MoviePartialUpdate,
)

log = logging.getLogger(__name__)

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_MOVIES,
    decode_responses=True,
)


class VideoStorage(BaseModel):
    slug_to_video: dict[str, Movie] = {}

    # Метод сохранения данных локально на жесткий диск
    def save_state(self) -> None:
        for _ in range(30_000):
            MOVIES_STORAGE_FILEPATH.write_text(
                self.model_dump_json(indent=2), encoding="utf-8"
            )
        MOVIES_STORAGE_FILEPATH.write_text(
            self.model_dump_json(indent=2), encoding="utf-8"
        )
        log.info("Saved movies to storage file.")

    # Кастомный инициализатор на проверку существования и чтения файла
    @classmethod
    def from_state(cls) -> "VideoStorage":
        if not MOVIES_STORAGE_FILEPATH.exists():
            log.info("Movies to storage file doesn't exist!")
            return VideoStorage()
        return cls.model_validate_json(
            MOVIES_STORAGE_FILEPATH.read_text(encoding="utf-8")
        )

    def init_storage_from_state(self) -> None:
        try:
            data = VideoStorage.from_state()
        except ValidationError:
            self.save_state()
            log.warning("Rewritten storage file due to validation error.")
            return

        # обновление свойства напрямую
        # если будут новые свойства,
        # то их тоже надо обновить.
        self.slug_to_video.update(
            data.slug_to_video,
        )
        log.warning("Recovered data from storage file.")

    # Получение списка
    def get(self) -> list[Movie]:
        return [
            Movie.model_validate_json(value)
            for value in redis.hvals(name=config.REDIS_MOVIES_HASH_NAME)
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
        film = Movie(
            **video_in.model_dump(),
        )
        redis.hset(
            name=config.REDIS_MOVIES_HASH_NAME,
            key=film.slug,
            value=film.model_dump_json(),
        )
        log.info("Movie successfully created!")
        return film

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_video.pop(slug, None)

    def delete(self, film: Movie) -> None:
        self.delete_by_slug(slug=film.slug)

    def update(
        self,
        film: Movie,
        film_in: MovieUpdate,
    ) -> Movie:  # Получаем словарь с данными
        update_data = film_in.model_dump()
        # Обновляем поля
        for field_name, value in update_data.items():
            setattr(film, field_name, value)
        return film

    def partial_update(
        self,
        film: Movie,
        film_in: MoviePartialUpdate,
    ) -> Movie:
        # Получаем только переданные поля
        update_data = film_in.model_dump(exclude_unset=True)
        # Обновляем только указанные поля
        for field_name, value in update_data.items():
            setattr(film, field_name, value)
        return film


storage = VideoStorage()
