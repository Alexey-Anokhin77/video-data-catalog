import pytest
from fastapi import status
from fastapi.testclient import TestClient

from main import app
from schemas.video_catalog import Movie


@pytest.mark.xfail(
    reason="not implemented yet",
    raises=NotImplementedError,
    strict=False,
)
@pytest.mark.apitest
def test_transfer_movie(
    movie: Movie,
    auth_client: TestClient,
) -> None:
    url = app.url_path_for(
        "transfer_film",
        slug=movie.slug,
    )
    response = auth_client.post(url)
    assert response.status_code == status.HTTP_200_OK, response.text
