from unittest import TestCase

from schemas.video_catalog import Movie, MovieCreate


class MovieCreateTestCase(TestCase):
    def test_move_can_be_created_from_create_schemas(self) -> None:
        movie_in = MovieCreate(
            slug="some-slug",
            title_film="some-title",
            genre="some-genre",
            description_film="some-description",
            time_film=120.5,
            production_year=1901,
        )

        movie = Movie(
            **movie_in.model_dump(),
        )

        self.assertEqual(
            movie_in.slug,
            movie.slug,
        )
        self.assertEqual(
            movie_in.description_film,
            movie.description_film,
        )
        self.assertEqual(
            movie_in.title_film,
            movie.title_film,
        )
        self.assertEqual(
            movie_in.genre,
            movie.genre,
        )
        self.assertEqual(
            movie_in.time_film,
            movie.time_film,
        )
        self.assertEqual(
            movie_in.production_year,
            movie.production_year,
        )
