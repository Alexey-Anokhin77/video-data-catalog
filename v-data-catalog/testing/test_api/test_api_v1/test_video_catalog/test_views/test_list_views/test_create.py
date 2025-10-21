import logging
import random
import string
from typing import Any

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from main import app
from schemas.video_catalog import Movie, MovieCreate
from testing.conftest import build_movie_create_random_slug

pytestmark = pytest.mark.apitest


def test_create_video(
    caplog: pytest.LogCaptureFixture,
    auth_client: TestClient,
) -> None:
    caplog.set_level(logging.INFO)
    movie = app.url_path_for("create_video")
    movie_create = MovieCreate(
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
    data: dict[str, str] = movie_create.model_dump(mode="json")
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
    assert "Movie successfully created" in caplog.text
    assert movie_create.slug in caplog.text


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


class TestCreateInvalid:

    @pytest.fixture(
        params=[
            pytest.param(("a", "string_too_short"), id="too-short"),
            pytest.param(("a" * 201, "string_too_long"), id="too-long"),
        ],
    )
    def movie_create_values(
        self,
        request: SubRequest,
    ) -> tuple[dict[str, Any], str]:
        build = build_movie_create_random_slug()
        data = build.model_dump(mode="json")
        slug, err_type = request.param
        data["slug"] = slug
        return data, err_type

    def test_invalid_slug(
        self,
        movie_create_values: tuple[dict[str, Any], str],
        auth_client: TestClient,
    ) -> None:
        movie = app.url_path_for("create_video")
        create_data, expected_error_type = movie_create_values
        response = auth_client.post(
            url=movie,
            json=create_data,
        )
        assert (
            response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        ), response.text
        error_detail = response.json()["detail"][0]
        assert error_detail["type"] == expected_error_type, error_detail
