from fastapi import APIRouter, Depends

from app.api.deps import get_current_active_user
from app.models import UserModel
from app.schemas import UserReadSchema

router = APIRouter()


@router.get("/profile")
async def get_current_user(
    user: UserModel = Depends(get_current_active_user),
) -> UserReadSchema:
    return user
