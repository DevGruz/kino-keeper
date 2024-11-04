from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_register(client):
    response = await client.post(
        "/register", json={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"


@pytest.mark.asyncio
async def test_register_with_employed_username(client):
    response = await client.post(
        "/register", json={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "REGISTER_USER_ALREADY_EXISTS"


@pytest.mark.asyncio
async def test_login(client: AsyncClient):
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
    assert "access_token" in response.cookies
    assert response.cookies["access_token"] is not None



@pytest.mark.asyncio
async def test_logout(logged_in_client: AsyncClient):
    assert logged_in_client.cookies.get("access_token")
    response = await logged_in_client.post("/logout")
    assert response.status_code == 204

