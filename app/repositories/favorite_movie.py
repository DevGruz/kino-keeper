from sqlalchemy import delete, insert, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import FavoriteMovieModel


class FavoriteMovieRepository:
    model = FavoriteMovieModel

    @classmethod
    async def add_one(cls, session: AsyncSession, **data):
        try:
            stmt = insert(cls.model).values(**data).returning(cls.model)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one_or_none()
        except SQLAlchemyError:
            await session.rollback()

    @classmethod
    async def find_all(cls, session: AsyncSession, **filter_by):
        try:
            stmt = select(cls.model).filter_by(**filter_by)
            result = await session.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError:
            ...

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filter_by):
        try:
            stmt = select(cls.model).filter_by(**filter_by)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError:
            ...

    @classmethod
    async def delete_one(cls, session: AsyncSession, **filter_by):
        try:
            stmt = delete(cls.model).filter_by(**filter_by).returning(cls.model)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one_or_none()
        except SQLAlchemyError:
            await session.rollback()
