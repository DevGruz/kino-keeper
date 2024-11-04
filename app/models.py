import uuid

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import JSON, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class BaseModel(DeclarativeBase): ...


class UserModel(SQLAlchemyBaseUserTableUUID, BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=True
    )
    username: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)

    favorite_movies: Mapped[list["FavoriteMovieModel"]] = relationship(
        "FavoriteMovieModel", back_populates="user"
    )


class FavoriteMovieModel(BaseModel):
    __tablename__ = "favorite_movies"

    id: Mapped[int] = mapped_column(primary_key=True)
    kinopoisk_id: Mapped[int] = mapped_column(nullable=False)
    movie_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    user: Mapped["UserModel"] = relationship(back_populates="favorite_movies")
