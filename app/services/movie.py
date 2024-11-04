from fastapi import HTTPException, status
from pydantic import ValidationError
from pydantic_core import from_json

from app.core.db import AsyncSession
from app.repositories.favorite_movie import FavoriteMovieRepository
from app.schemas.movie import MovieDetailSchema, SeachMoviesByKeywordSchema
from app.schemas.user import UserReadSchema
from app.utils import KinopoiskAPIClient


class MovieService:
    def __init__(
        self,
        repository: FavoriteMovieRepository,
        session: AsyncSession,
        api_client: KinopoiskAPIClient,
    ):
        self.repository = repository
        self.session = session
        self.api_client = api_client

    async def search_movies(self, query: str) -> SeachMoviesByKeywordSchema:
        data = await self.api_client.search_movies(query)
        try:
            return SeachMoviesByKeywordSchema.model_validate(data)
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid movie data format.",
            ) from e

    async def get_movie_details(self, kinopoisk_id: int) -> MovieDetailSchema:
        data = await self.api_client.get_movie_details(kinopoisk_id)
        try:
            return MovieDetailSchema.model_validate(data)
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid movie data format.",
            ) from e

    async def add_to_favorites(
        self, *, user: UserReadSchema, kinopoisk_id: int
    ) -> MovieDetailSchema:
        existing_movie = await self.repository.find_one_or_none(
            self.session, user_id=user.id, kinopoisk_id=kinopoisk_id
        )

        if existing_movie:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Movie already in favorites.",
            )

        movie_details = await self.get_movie_details(kinopoisk_id)

        await self.repository.add_one(
            self.session,
            user_id=user.id,
            kinopoisk_id=kinopoisk_id,
            movie_data=movie_details.model_dump_json(by_alias=True),
        )

        return movie_details

    async def get_favorites(self, *, user: UserReadSchema) -> list[MovieDetailSchema]:
        favorites = await self.repository.find_all(self.session, user_id=user.id)
        return [self._parse_favorite_movie(fav.movie_data) for fav in favorites]

    async def remove_from_favorites(
        self, *, user: UserReadSchema, kinopoisk_id: int
    ) -> None:
        deleted = await self.repository.delete_one(
            self.session,
            user_id=user.id,
            kinopoisk_id=kinopoisk_id,
        )
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Favorite movie not found.",
            )

    def _parse_favorite_movie(self, movie_data_json: str) -> MovieDetailSchema:
        try:
            movie_data = from_json(movie_data_json)
            return MovieDetailSchema.model_validate(movie_data)
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid stored movie data format.",
            ) from e
