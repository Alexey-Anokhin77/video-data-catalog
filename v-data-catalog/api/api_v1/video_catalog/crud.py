from schemas.video_catalog import VideoCatalog

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
