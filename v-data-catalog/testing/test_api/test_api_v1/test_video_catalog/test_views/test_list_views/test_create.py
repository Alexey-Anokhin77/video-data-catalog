import random
import string

from fastapi import status
from fastapi.testclient import TestClient

from main import app
from schemas.video_catalog import Movie, MovieCreate


def test_create_video(auth_client: TestClient) -> None:
    movie = app.url_path_for("create_video")
    data: dict[str, str] = MovieCreate(
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
    ).model_dump(mode="json")
    response = auth_client.post(url=movie, json=data)
    assert response.status_code == status.HTTP_201_CREATED, response.text
    response_data = response.json()
    received_values = {
        "slug": response_data["slug"],
        "description_film": response_data["description_film"],
        "time_film": response_data["time_film"],
        "title_film": response_data["title_film"],
        "genre": response_data["genre"],
        "production_year": response_data["production_year"],
    }
    assert received_values == data, response_data


def test_create_movie_already_exists(
    auth_client: TestClient,
    movie: Movie,
) -> None:
    movie_create = MovieCreate(**movie.model_dump())
    data = movie_create.model_dump(mode="json")
    url = app.url_path_for("create_video")
    response = auth_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    response_data = response.json()
    expected_error_detail = f"Movie with slug={movie.slug!r} already exists"
    assert response_data["detail"] == expected_error_detail, response.text
