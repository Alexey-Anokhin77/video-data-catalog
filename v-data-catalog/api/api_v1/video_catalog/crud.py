from pydantic import BaseModel

from schemas.video_catalog import (
    Movie,
    MovieCreate,
    MovieUpdate,
)

FILM_CATALOG = [
    Movie(
        slug="interstellar-2014",
        title_film="Интерстеллар",
        description_film="about",
        time_film=2.50,
    ),
    Movie(
        slug="the-matrix-1999",
        title_film="Матрица",
        description_film="Хакер узнаёт, что мир вокруг — иллюзия, созданная искусственным разумом, "
        "и присоединяется к борьбе за освобождение человечества от машинного контроля.",
        time_film=2.45,
    ),
    Movie(
        slug="Inception 2010",
        title_film="Начало",
        description_film="Группа специалистов проникает в подсознание людей, используя технику погружения в "
        "сновидения.",
        time_film=2.28,
    ),
]


class VideosStorage(BaseModel):
    slug_to_video: dict[str, Movie] = {}

    # Получение списка
    def get(self) -> list[Movie]:
        return list(self.slug_to_video.values())

    # Получение по slug
    def get_by_slug(self, slug: str) -> Movie | None:
        return self.slug_to_video.get(slug)

    # Создание нового видео
    def create(self, video_in: MovieCreate) -> Movie:
        film = Movie(
            **video_in.model_dump(),
        )
        self.slug_to_video[film.slug] = film
        return film

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_video.pop(slug, None)

    def delete(self, film: Movie) -> None:
        self.delete_by_slug(slug=film.slug)

    def update(
        self,
        movie: Movie,
        film_in: MovieUpdate,
    ) -> Movie:
        for field_name, value in film_in:
            setattr(movie, field_name, value)
        return movie


storage = VideosStorage()

storage.create(
    MovieCreate(
        slug="interstellar-2014",
        title_film="Интерстеллар",
        description_film="Фильм «Интерстеллар» рассказывает историю группы астронавтов, отправившихся сквозь "
        "червоточину в космос в поисках нового дома для человечества, столкнувшегося с угрозой "
        "голода и истощения ресурсов Земли.",
        time_film=2.50,
    ),
)
storage.create(
    MovieCreate(
        slug="the-matrix-1999",
        title_film="Матрица",
        description_film="Хакер узнаёт, что мир вокруг — иллюзия, созданная искусственным разумом, "
        "и присоединяется к борьбе за освобождение человечества от машинного контроля.",
        time_film=2.45,
    ),
)
storage.create(
    MovieCreate(
        slug="Inception 2010",
        title_film="Начало",
        description_film="Группа специалистов проникает в подсознание людей, используя технику погружения в "
        "сновидения.",
        time_film=2.28,
    ),
)
