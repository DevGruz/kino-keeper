import pytest


@pytest.mark.asyncio
async def test_get_user_profile(logged_in_client):
    response = await logged_in_client.get("/profile")
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
