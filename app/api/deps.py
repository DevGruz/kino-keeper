import uuid

from fastapi import Depends
from fastapi_users import FastAPIUsers

from app.core.auth import auth_backend_bearer, auth_backend_cookie
from app.core.db import AsyncSession, get_async_session
from app.models import UserModel
from app.repositories import FavoriteMovieRepository, UserRepository
from app.services import MovieService, UserService
from app.utils import KinopoiskAPIClient


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield UserRepository(session, UserModel)


async def get_user_service(user_db: UserRepository = Depends(get_user_db)):
    yield UserService(user_db)


async def get_favorite_movie_repository():
    return FavoriteMovieRepository()


async def get_kinopoisk_api_client():
    return KinopoiskAPIClient()


async def get_movie_service(
    repository: FavoriteMovieRepository = Depends(get_favorite_movie_repository),
    session: AsyncSession = Depends(get_async_session),
    api_client: KinopoiskAPIClient = Depends(get_kinopoisk_api_client),
):
    yield MovieService(
        repository=repository,
        session=session,
        api_client=api_client,
    )


fastapi_users = FastAPIUsers[UserModel, uuid.UUID](
    get_user_service, [auth_backend_cookie, auth_backend_bearer]
)

_current_active_user = fastapi_users.current_user(active=True)


async def get_current_active_user(current_active_user=Depends(_current_active_user)):
    return current_active_user
