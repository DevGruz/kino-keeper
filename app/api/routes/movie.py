from fastapi import APIRouter, Depends, status

from app.api.deps import MovieService, get_current_active_user, get_movie_service
from app.schemas import MovieDetailSchema, SeachMoviesByKeywordSchema, UserReadSchema

router = APIRouter()


@router.get("/search", response_model=SeachMoviesByKeywordSchema)
async def search_movies(
    query: str,
    movie_service: MovieService = Depends(get_movie_service),
):
    data = await movie_service.search_movies(query=query)
    return data


@router.get("/{kinopoisk_id:int}", response_model=MovieDetailSchema)
async def get_movie_details(
    kinopoisk_id: int,
    movie_service: MovieService = Depends(get_movie_service),
):
    data = await movie_service.get_movie_details(kinopoisk_id=kinopoisk_id)
    return data


@router.get("/favorites", response_model=list[MovieDetailSchema])
async def get_user_favorites(
    user: UserReadSchema = Depends(get_current_active_user),
    movie_service: MovieService = Depends(get_movie_service),
):
    data = await movie_service.get_favorites(user=user)
    return data


@router.post(
    "/favorites",
    status_code=status.HTTP_201_CREATED,
    response_model=MovieDetailSchema,
)
async def add_movie_to_favorites(
    kinopoisk_id: int,
    user: UserReadSchema = Depends(get_current_active_user),
    movie_service: MovieService = Depends(get_movie_service),
):
    data = await movie_service.add_to_favorites(user=user, kinopoisk_id=kinopoisk_id)
    return data


@router.delete("/favorites/{kinopoisk_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie_from_favorites(
    kinopoisk_id: int,
    user: UserReadSchema = Depends(get_current_active_user),
    movie_service: MovieService = Depends(get_movie_service),
):
    await movie_service.remove_from_favorites(user=user, kinopoisk_id=kinopoisk_id)
