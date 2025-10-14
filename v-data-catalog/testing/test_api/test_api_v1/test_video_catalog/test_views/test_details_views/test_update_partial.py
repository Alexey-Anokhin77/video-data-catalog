from collections.abc import Generator
from datetime import UTC, datetime

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from api.api_v1.video_catalog.crud import storage
from main import app
from schemas.video_catalog import DESCRIPTION_MAX_LENGTH, Movie
from testing.conftest import movie_create_random_slug


@pytest.mark.apitest
class TestUpdatePartial:

    CURRENT_YEAR = datetime.now(UTC).year
    MIN_YEAR = 1900

    @pytest.fixture()
    def movie(self, request: SubRequest) -> Generator[Movie]:
        production_year, description_film = request.param
        # return movie_create_random_slug(
        #     description_film=description_film,
        #     production_year=production_year,
        # )

        # Валидация года
        if not (self.MIN_YEAR <= production_year <= self.CURRENT_YEAR):
            pytest.fail(
                f"Год {production_year} должен быть между "
                f"{self.MIN_YEAR} и {self.CURRENT_YEAR}",
            )

        movie = movie_create_random_slug(
            description_film=description_film,
            production_year=production_year,
        )
        yield movie
        storage.delete(movie)

    @pytest.mark.parametrize(
        "movie, new_description",
        [
            pytest.param(
                (MIN_YEAR, "Some description"),
                "",
                id="old_film_and_no_description",
            ),
            pytest.param(
                (CURRENT_YEAR, ""),
                "some_description",
                id="new_film_and_some_description",
            ),
            pytest.param(
                (MIN_YEAR, "a" * DESCRIPTION_MAX_LENGTH),
                "",
                id="new_film_and_max_description_to_no_description",
            ),
            pytest.param(
                (CURRENT_YEAR, ""),
                "a" * DESCRIPTION_MAX_LENGTH,
                id="old_film_and_no_description_to_max_description",
            ),
        ],
        indirect=["movie"],
    )
    def test_update_movie_partial(
        self,
        movie: Movie,
        auth_client: TestClient,
        new_description: str,
    ) -> None:
        film = app.url_path_for(
            "update_movie_details_partial",
            slug=movie.slug,
        )
        response = auth_client.patch(film, json={"description_film": new_description})
        assert response.status_code == status.HTTP_200_OK, response.text

        new_production_year = movie.production_year + 1

        response = auth_client.patch(
            film,
            json={"production_year": new_production_year},
        )
        assert response.status_code == status.HTTP_200_OK, response.text

        movie_db = storage.get_by_slug(movie.slug)
        assert movie_db
        assert movie_db.description_film == new_description
        assert movie_db.description_film != movie.description_film
        assert movie_db.production_year == new_production_year
