from schemas.video_catalog import VideoCatalog

FILM_CATALOG = [
    VideoCatalog(
        id_film=1,
        title_film="Интерстеллар",
        description_film="Команда астронавтов отправляется сквозь червоточину в поисках нового дома для "
        "пределов человеческой выносливости.",
        time_film=2.50,
    ),
    VideoCatalog(
        id_film=2,
        title_film="Матрица",
        description_film="Хакер узнаёт, что мир вокруг — иллюзия, созданная искусственным разумом, "
        "и присоединяется к борьбе за освобождение человечества от машинного контроля.",
        time_film=2.45,
    ),
    VideoCatalog(
        id_film=3,
        title_film="Начало",
        description_film="Группа специалистов проникает в подсознание людей, используя технику погружения в "
        "сновидения.",
        time_film=2.28,
    ),
]
