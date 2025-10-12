import logging
from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from starlette import status
from starlette.testclient import TestClient

from api.api_v1.video_catalog.crud import storage
from main import app
from schemas.video_catalog import Movie, MovieUpdate
from testing.conftest import movie_create_random_slug

logger = logging.getLogger(__name__)


class TestUpdate:

    @pytest.fixture()
    def movie(self, request: SubRequest) -> Generator[Movie]:
        title_film, description_film = request.param
        logger.info("🛠️  СОЗДАНИЕ ФИЛЬМА В ФИКСТУРЕ")
        logger.info("   Исходный title: '%s'", title_film)
        logger.info("   Исходный description: '%s'", description_film)

        movie = movie_create_random_slug(
            title_film=title_film,
            description_film=description_film,
        )

        logger.info("   Фильм создан: Slug=%s", movie.slug)
        logger.info(
            "   Genre: '%s', Year: %s, Time: %s мин",
            movie.genre,
            movie.production_year,
            movie.time_film,
        )

        yield movie

        logger.info("🧹 УДАЛЕНИЕ ФИЛЬМА: %s", movie.slug)
        storage.delete(movie)

    @pytest.mark.parametrize(
        "movie, new_title, new_description",
        [
            pytest.param(
                ("some title", "some description"),
                "update title",
                "some description",
                id="some-description-and-new-title",
            ),
        ],
        indirect=["movie"],
    )
    def test_update_movie_details(
        self,
        movie: Movie,
        new_title: str,
        new_description: str,
        auth_client: TestClient,
    ) -> None:
        logger.info("🎬 НАЧАЛО ТЕСТА: Обновление данных фильма")
        logger.info("=" * 60)

        # Логируем исходные данные
        logger.info("📋 ИСХОДНЫЕ ДАННЫЕ ФИЛЬМА:")
        logger.info("   • Title: '%s'", movie.title_film)
        logger.info("   • Description: '%s'", movie.description_film)
        logger.info("   • Genre: '%s'", movie.genre)
        logger.info("   • Production Year: %s", movie.production_year)
        logger.info("   • Time: %s мин", movie.time_film)
        logger.info("   • Slug: %s", movie.slug)

        film = app.url_path_for(
            "update_movie_details",
            slug=movie.slug,
        )

        # Логируем данные для обновления
        logger.info("🔄 ДАННЫЕ ДЛЯ ОБНОВЛЕНИЯ:")
        logger.info("   • Новый Title: '%s'", new_title)
        logger.info("   • Новый Description: '%s'", new_description)
        logger.info("   • Genre (без изменений): '%s'", movie.genre)
        logger.info("   • Production Year (без изменений): %s", movie.production_year)
        logger.info("   • Time (без изменений): %s мин", movie.time_film)

        update = MovieUpdate(
            title_film=new_title,
            description_film=new_description,
            genre=movie.genre,
            production_year=movie.production_year,
            time_film=movie.time_film,
        )

        logger.info("🌐 ОТПРАВКА PUT-ЗАПРОСА...")
        response = auth_client.put(
            film,
            json=update.model_dump(mode="json"),
        )

        logger.info("📡 ПОЛУЧЕН ОТВЕТ: %s", response.status_code)
        assert response.status_code == status.HTTP_200_OK, response.text

        logger.info("✅ ЗАПРОС УСПЕШЕН, ПРОВЕРЯЕМ ДАННЫЕ В БАЗЕ...")
        movie_db = storage.get_by_slug(movie.slug)
        assert movie_db

        # Логируем результат
        logger.info("📊 РЕЗУЛЬТАТ ОБНОВЛЕНИЯ:")
        logger.info(
            "   • Title: '%s' (было: '%s')",
            movie_db.title_film,
            movie.title_film,
        )
        logger.info(
            "   • Description: '%s' (было: '%s')",
            movie_db.description_film,
            movie.description_film,
        )
        logger.info("   • Genre: '%s' (без изменений)", movie_db.genre)
        logger.info(
            "   • Production Year: %s (без изменений)",
            movie_db.production_year,
        )
        logger.info("   • Time: %s мин (без изменений)", movie_db.time_film)

        # Проверяем через модель
        new_data = MovieUpdate(**movie_db.model_dump())

        logger.info("🔍 ПРОВЕРКА РАВЕНСТВА МОДЕЛЕЙ...")
        assert new_data == update
        logger.info("✅ МОДЕЛИ СОВПАДАЮТ")

        logger.info("🎉 ТЕСТ УСПЕШНО ЗАВЕРШЕН!")
        logger.info("=" * 60)
