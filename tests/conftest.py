from typing import AsyncGenerator
from httpx import ASGITransport, AsyncClient
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.core.db import get_async_session
from app.main import app
from app.models import BaseModel


async_engine_test = create_async_engine(
    url=settings.DATABASE_TEST.URL, poolclass=NullPool
)
async_session_maker = async_sessionmaker(
    async_engine_test, expire_on_commit=False, autocommit=False
)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    async with async_engine_test.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    yield
    async with async_engine_test.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest.fixture
async def logged_in_client(client: AsyncClient):
    response = await client.post(
        "/login",
        data={
            "grant_type": "password",
            "username": "testuser",
            "password": "testpass",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 204
    client.cookies.clear()
    client.cookies.set("access_token", response.cookies["access_token"])
    return client
