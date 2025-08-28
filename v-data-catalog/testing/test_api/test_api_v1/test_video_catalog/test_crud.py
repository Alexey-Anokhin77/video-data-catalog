import random
import string
from os import getenv
from unittest import TestCase

from api.api_v1.video_catalog.crud import storage
from schemas.video_catalog import (
    Movie,
    MovieCreate,
    MoviePartialUpdate,
    MovieUpdate,
)

if getenv("TESTING") != "1":
    msg = "Environment is not ready for testing"
    raise OSError(msg)


def total(a: int, b: int) -> int:
    return a + b


class VideoStorageUpdateTestCase(TestCase):
    def setUp(self) -> None:
        self.movie = self.create_movie()

    def tearDown(self) -> None:
        storage.delete(self.movie)

    def create_movie(self) -> Movie:
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
            description_film=self.movie.description_film * 2,
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
