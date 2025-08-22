from unittest import TestCase

from pydantic import ValidationError

from schemas.video_catalog import Movie, MovieCreate, MoviePartialUpdate, MovieUpdate


class MovieCreateTestCase(TestCase):
    def test_movie_can_be_created_from_create_schemas(self) -> None:
        movie_in = MovieCreate(
            slug="some-slug",
            title_film="some-title",
            genre="some-genre",
            description_film="some-description",
            time_film=120.5,
            production_year=1901,
        )

        movie = Movie(
            **movie_in.model_dump(),
        )

        self.assertEqual(
            movie_in.slug,
            movie.slug,
        )
        self.assertEqual(
            movie_in.description_film,
            movie.description_film,
        )
        self.assertEqual(
            movie_in.title_film,
            movie.title_film,
        )
        self.assertEqual(
            movie_in.genre,
            movie.genre,
        )
        self.assertEqual(
            movie_in.time_film,
            movie.time_film,
        )
        self.assertEqual(
            movie_in.production_year,
            movie.production_year,
        )

    def test_movie_create_accepts_different_values(self) -> None:
        test_movie_data = {
            "title_film": "Test Title",
            "time_film": 120.0,
            "genre": "Test Genre",
            "production_year": 2023,
        }
        test_case = [
            {
                "slug": "edge-case-1",
                "description": "X" * 1000,  # Максимальная длина
                "expected_len": 1000,  # Явная проверка граничного значения
            },
            {
                "slug": "edge-case-2",
                "description": "X",  # Минимальная длина
                "expected_len": 1,
            },
        ]

        for case in test_case:
            with self.subTest(case=case):
                movie = MovieCreate(
                    slug=case["slug"],
                    description_film=case["description"],
                    **test_movie_data,
                )

                self.assertEqual(movie.slug, case["slug"])
                self.assertEqual(movie.description_film, case["description"])
                self.assertEqual(len(movie.description_film), case["expected_len"])

    # Тест на проверку длины slug, что он не больше 10
    def test_movie_slug_too_short_(self) -> None:
        with self.assertRaises(ValidationError) as exc_info:
            MovieCreate(
                slug="a",
                title_film="some-title",
                genre="some-genre",
                description_film="some-description",
                time_film=120.5,
                production_year=1901,
            )

        # print(exc_info.exception)
        # print(exc_info.exception.json())
        # print(exc_info.exception.errors())

        errors_details = exc_info.exception.errors()[0]
        expected_types = "string_too_short"
        self.assertEqual(
            expected_types,
            errors_details["type"],
        )

    def test_movie_slug_too_short_with_regex(self) -> None:
        with self.assertRaisesRegex(
            ValidationError,
            expected_regex="String should have at least 3 characters",
        ):
            MovieCreate(
                slug="a",
                title_film="some-title",
                genre="some-genre",
                description_film="some-description",
                time_film=120.5,
                production_year=1901,
            )


class MovieUpdateTestCase(TestCase):
    def test_movie_can_be_updated_from_update_schemas(self) -> None:
        # logging.basicConfig(level=logging.INFO)
        # 1. Создаем исходный фильм (аналог movie_in в тесте создания)
        original_movie = Movie(
            slug="original-slug",
            title_film="original-title",
            genre="original-genre",
            description_film="original-description",
            time_film=90.0,
            production_year=2000,
            notes="original-notes",
        )

        # 2. Создаем данные для обновления (аналог MovieCreate в тесте создания)
        update_data = MovieUpdate(
            title_film="updated-title",
            genre="updated-genre",
            description_film="updated-description",
            time_film=120.5,
            production_year=2023,
        )

        # 3. Обновляем фильм (вместо создания нового)
        updated_movie = original_movie.model_copy(
            update=update_data.model_dump(exclude_unset=True),
        )

        # logging.info("Результат обновления: %s", updated_movie)

        # 4. Проверяем обновленные поля (аналогично тесту создания)
        self.assertEqual(update_data.title_film, updated_movie.title_film)
        self.assertEqual(update_data.description_film, updated_movie.description_film)
        self.assertEqual(update_data.genre, updated_movie.genre)
        self.assertEqual(update_data.time_film, updated_movie.time_film)
        self.assertEqual(update_data.production_year, updated_movie.production_year)

        # 5. Проверяем, что slug и notes не изменились
        self.assertEqual(original_movie.slug, updated_movie.slug)
        self.assertEqual(original_movie.notes, updated_movie.notes)


class MoviePartialUpdateTestCase(TestCase):
    def test_movie_can_be_partial_updated_from_update_schemas(self) -> None:
        # logging.basicConfig(level=logging.INFO)
        original_movie = Movie(
            slug="original-slug",
            title_film="original-title",
            genre="some-genre",
            description_film="some-description",
            time_film=120.5,
            production_year=1901,
        )

        movie_partial_update = MoviePartialUpdate(
            genre="updated-genre",
            time_film=121.5,
        )

        updated_partial_movie = original_movie.model_copy(
            update=movie_partial_update.model_dump(exclude_unset=True),
        )

        # logging.info("Результат обновления: %s", movie_partial_update)
        # logging.info("Оригинал: %s", original_movie)
        # logging.info("Обновлённый: %s", updated_partial_movie)

        self.assertEqual(updated_partial_movie.genre, "updated-genre")
        self.assertEqual(updated_partial_movie.title_film, original_movie.title_film)
        self.assertEqual(
            updated_partial_movie.description_film,
            original_movie.description_film,
        )
        self.assertEqual(updated_partial_movie.time_film, 121.5)
        self.assertEqual(
            updated_partial_movie.production_year,
            original_movie.production_year,
        )
