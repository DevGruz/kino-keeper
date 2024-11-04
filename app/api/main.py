from fastapi import APIRouter, Depends

from app.api.deps import get_current_active_user
from app.api.routes import auth, movie, user

api_router = APIRouter()

api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(user.router, tags=["users"])
api_router.include_router(
    movie.router,
    prefix="/movies",
    tags=["movies"],
    dependencies=[Depends(get_current_active_user)],
)
