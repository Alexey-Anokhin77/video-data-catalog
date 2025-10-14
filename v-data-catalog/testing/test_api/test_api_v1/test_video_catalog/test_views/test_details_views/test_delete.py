import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from api.api_v1.video_catalog.crud import storage
from main import app
from schemas.video_catalog import Movie
from testing.conftest import create_movie


@pytest.fixture(
    params=[
        pytest.param("some-slug", id="some-slug"),
        pytest.param("slug", id="slug"),
        pytest.param("abc", id="min-slug"),
        pytest.param("abc-qwerty", id="max-slug"),
    ],
)
def movie(request: SubRequest) -> Movie:
    return create_movie(request.param)


@pytest.mark.apitest
def test_delete(
    movie: Movie,
    auth_client: TestClient,
) -> None:
    movies = app.url_path_for(
        "delete_film",
        slug=movie.slug,
    )
    response = auth_client.delete(movies)
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.text
    assert not storage.exists(movie.slug)
