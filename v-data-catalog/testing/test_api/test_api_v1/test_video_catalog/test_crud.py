import random
import string
from typing import ClassVar
from unittest import TestCase

from api.api_v1.video_catalog.crud import storage
from schemas.video_catalog import (
    Movie,
    MovieCreate,
    MoviePartialUpdate,
    MovieUpdate,
)


def create_movie() -> Movie:
    movie_in = MovieCreate(
        slug="".join(
            random.choices(
                string.ascii_letters,
                k=8,
            ),
        ),
        description_film="Some description",
        time_film=1,
        title_film="Some Title",
        genre="Some Genre",
        production_year=1901,
    )
    return storage.create(movie_in)


class VideoStorageUpdateTestCase(TestCase):
    def setUp(self) -> None:
        self.movie = create_movie()

    def tearDown(self) -> None:
        storage.delete(self.movie)

    def test_update(self) -> None:
        movie_update = MovieUpdate(
            **self.movie.model_dump(),
        )
        source_description = self.movie.description_film
        movie_update.description_film *= 2
        updated_movie = storage.update(
            movie=self.movie,
            movie_in=movie_update,
        )

        self.assertNotEqual(
            source_description,
            updated_movie.description_film,
        )

        self.assertEqual(
            movie_update,
            MovieUpdate(**updated_movie.model_dump()),
        )

    def test_partial_update(self) -> None:
        movie_partial_update = MoviePartialUpdate(
            description_film=self.movie.description_film * 3,
        )
        source_description = self.movie.description_film
        updated_movie = storage.partial_update(
            movie=self.movie,
            movie_in=movie_partial_update,
        )

        self.assertNotEqual(
            source_description,
            updated_movie.description_film,
        )

        self.assertEqual(
            movie_partial_update.description_film,
            updated_movie.description_film,
        )


class VideoStorageGetMoviesTestCase(TestCase):
    MOVIES_COUNT = 3
    movies: ClassVar[list[Movie]] = []

    @classmethod
    def setUpClass(cls) -> None:
        cls.movies = [create_movie() for _ in range(cls.MOVIES_COUNT)]

    @classmethod
    def tearDownClass(cls) -> None:
        for movie in cls.movies:
            storage.delete(movie)

    def test_get_list(self) -> None:
        movies = storage.get()
        # expected_slugs = {mvs.slug for mvs in self.movies}
        slugs = {mvs.slug for mvs in movies}
        expected_diff = set[str]()
        diff = expected_diff - slugs
        self.assertEqual(expected_diff, diff)

    def test_get_by_slug(self) -> None:
        for movie in self.movies:
            with self.subTest(
                slug=movie.slug,
                msg=f"Validate can get slug {movie!r}",
            ):
                db_movies = storage.get_by_slug(movie.slug)
                self.assertEqual(
                    movie,
                    db_movies,
                )
