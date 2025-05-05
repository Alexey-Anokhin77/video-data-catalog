from pydantic import BaseModel

from schemas.video_catalog import (
    VideoCatalog,
    VideoCreate,
)

FILM_CATALOG = [
    VideoCatalog(
        slug="interstellar-2014",
        title_film="Интерстеллар",
        description_film="about",
        time_film=2.50,
    ),
    VideoCatalog(
        slug="the-matrix-1999",
        title_film="Матрица",
        description_film="Хакер узнаёт, что мир вокруг — иллюзия, созданная искусственным разумом, "
        "и присоединяется к борьбе за освобождение человечества от машинного контроля.",
        time_film=2.45,
    ),
    VideoCatalog(
        slug="Inception 2010",
        title_film="Начало",
        description_film="Группа специалистов проникает в подсознание людей, используя технику погружения в "
        "сновидения.",
        time_film=2.28,
    ),
]


class VideosStorage(BaseModel):
    slug_to_video: dict[str, VideoCatalog] = {}

    # Получение списка
    def get(self) -> list[VideoCatalog]:
        return list(self.slug_to_video.values())

    # Получение по slug
    def get_by_slug(self, slug: str) -> VideoCatalog | None:
        return self.slug_to_video.get(slug)

    # Создание нового видео
    def create(self, video_in: VideoCreate) -> VideoCatalog:
        film = VideoCatalog(
            **video_in.model_dump(),
        )
        self.slug_to_video[film.slug] = film
        return film

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_video.pop(slug, None)

    def delete(self, film: VideoCatalog) -> None:
        self.delete_by_slug(slug=film.slug)


storage = VideosStorage()

storage.create(
    VideoCreate(
        slug="interstellar-2014",
        title_film="Интерстеллар",
        description_film="about",
        time_film=2.50,
    ),
)
storage.create(
    VideoCreate(
        slug="the-matrix-1999",
        title_film="Матрица",
        description_film="Хакер узнаёт, что мир вокруг — иллюзия, созданная искусственным разумом, "
        "и присоединяется к борьбе за освобождение человечества от машинного контроля.",
        time_film=2.45,
    ),
)
storage.create(
    VideoCreate(
        slug="Inception 2010",
        title_film="Начало",
        description_film="Группа специалистов проникает в подсознание людей, используя технику погружения в "
        "сновидения.",
        time_film=2.28,
    ),
)
