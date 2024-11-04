from fastapi import APIRouter

from app.api.deps import auth_backend_bearer, auth_backend_cookie, fastapi_users
from app.schemas import UserCreateSchema, UserReadSchema

router = APIRouter()


router.include_router(
    fastapi_users.get_register_router(UserReadSchema, UserCreateSchema),
)
router.include_router(
    fastapi_users.get_auth_router(auth_backend_bearer),
    include_in_schema=False,
    prefix="/bearer",
)
router.include_router(
    fastapi_users.get_auth_router(auth_backend_cookie),
)
