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


def build_movie_create(
    slug: str,
    description_film: str = "Some description",
    production_year: int = 1901,
    title_film: str = "Some Title",
) -> MovieCreate:
    return MovieCreate(
        slug=slug,
        description_film=description_film,
        time_film=1,
        title_film=title_film,
        genre="Some Genre",
        production_year=production_year,
    )


def build_movie_create_random_slug(
    description_film: str = "Some description",
    production_year: int = 1901,
    title_film: str = "Some Title",
) -> MovieCreate:
    return build_movie_create(
        slug="".join(
            random.choices(
                string.ascii_letters,
                k=8,
            ),
        ),
        description_film=description_film,
        production_year=production_year,
        title_film=title_film,
    )


def create_movie(
    slug: str,
    description_film: str = "Some description",
) -> Movie:
    movie_in = build_movie_create(
        slug=slug,
        description_film=description_film,
    )
    return storage.create(movie_in)


def movie_create_random_slug(
    description_film: str = "Some description",
    production_year: int = 1901,
    title_film: str = "Some Title",
) -> Movie:
    movie_in = build_movie_create_random_slug(
        description_film=description_film,
        production_year=production_year,
        title_film=title_film,
    )
    return storage.create(movie_in)


@pytest.fixture()
def movie() -> Generator[Movie]:
    movie = movie_create_random_slug()
    yield movie
    storage.delete(movie)
