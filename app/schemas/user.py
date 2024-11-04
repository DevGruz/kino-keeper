import re
import uuid
from typing import Optional

from fastapi_users import schemas
from pydantic import EmailStr, Field, field_validator

USERNAME_REGEX = re.compile(r"^[a-zA-Z0-9_.-]{3,20}$")


class UserReadSchema(schemas.BaseUser[uuid.UUID]):
    email: Optional[EmailStr] = None
    username: str


class UserCreateSchema(schemas.CreateUpdateDictModel):
    username: str = Field(min_length=3, max_length=20)
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if not USERNAME_REGEX.match(value):
            raise ValueError(
                "Username must contain only letters, numbers, dots, underscores, or hyphens, and be 3-20 characters long."
            )
        return value
