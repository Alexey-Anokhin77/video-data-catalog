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


def build_movie_create(slug: str) -> MovieCreate:
    return MovieCreate(
        slug=slug,
        description_film="Some description",
        time_film=1,
        title_film="Some Title",
        genre="Some Genre",
        production_year=1901,
    )


def build_movie_create_random_slug() -> MovieCreate:
    return build_movie_create(
        slug="".join(
            random.choices(
                string.ascii_letters,
                k=8,
            ),
        ),
    )


def create_movie(slug: str) -> Movie:
    movie_in = build_movie_create(slug=slug)
    return storage.create(movie_in)


def movie_create_random_slug() -> Movie:
    movie_in = build_movie_create_random_slug()
    return storage.create(movie_in)


@pytest.fixture()
def movie() -> Generator[Movie]:
    movie = movie_create_random_slug()
    yield movie
    storage.delete(movie)
