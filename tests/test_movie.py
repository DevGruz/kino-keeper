import pytest


@pytest.mark.asyncio
async def test_search_movies(logged_in_client):
    response = await logged_in_client.get("/movies/search", params={"query": "Начало"})
    assert response.status_code == 200
    assert "query" in response.json()
    assert "films" in response.json()
    assert len(response.json()["films"]) > 0


@pytest.mark.asyncio
async def test_get_movie_details(logged_in_client):
    response = await logged_in_client.get("/movies/12345")
    assert response.status_code == 200
    assert "kinopoiskId" in response.json()
    assert response.json()["kinopoiskId"] == 12345


@pytest.mark.asyncio
async def test_add_to_favorites(logged_in_client):
    response_1 = await logged_in_client.post(
        "/movies/favorites",
        params={"kinopoisk_id": 12345},
    )
    assert response_1.status_code == 201
    assert response_1.json()["kinopoiskId"] == 12345

    response_2 = await logged_in_client.post(
        "/movies/favorites",
        params={"kinopoisk_id": 311121},
    )

    assert response_2.status_code == 201
    assert response_2.json()["kinopoiskId"] == 311121


@pytest.mark.asyncio
async def test_get_favorites(logged_in_client):
    response = await logged_in_client.get(
        "/movies/favorites",
    )
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_remove_from_favorites(logged_in_client):
    response = await logged_in_client.delete(
        "/movies/favorites/12345",
    )
    assert response.status_code == 204
