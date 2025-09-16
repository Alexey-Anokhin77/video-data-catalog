import random
import string
from collections.abc import Generator
from os import getenv

import pytest

from api.api_v1.video_catalog.crud import storage
from schemas.video_catalog import Movie, MovieCreate

if getenv("TESTING") != "1":
    msg = "Environment is not ready for testing"
    pytest.exit(msg)


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


@pytest.fixture()
def movie() -> Generator[Movie]:
    movie = create_movie()
    yield movie
    storage.delete(movie)
