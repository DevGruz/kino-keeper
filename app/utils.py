from typing import Any

import httpx
from fastapi import HTTPException, status

from app.core.config import settings


class KinopoiskAPIClient:
    def __init__(
        self,
        api_key: str = settings.KINOPOISK_UNOFFICIAL_API_KEY,
        base_url: str = settings.KINOPOISK_UNOFFICIAL_URL,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json",
        }

    async def search_movies(self, query: str) -> list[dict[str, Any]]:
        url = f"{self.base_url}/api/v2.1/films/search-by-keyword"
        params = {"keyword": query}
        return await self._make_request("GET", url, params=params)

    async def get_movie_details(self, kinopoisk_id: int) -> dict:
        url = f"{self.base_url}/api/v2.2/films/{kinopoisk_id}"
        return await self._make_request("GET", url)

    async def _make_request(self, method: str, url: str, params: dict = None) -> dict:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method, url, headers=self.headers, params=params
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Film not found on Kinopoisk.",
                    )
                if e.response.status_code == status.HTTP_400_BAD_REQUEST:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid request parameters.",
                    )
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Error retrieving data from Kinopoisk.",
                )
            except httpx.RequestError:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Kinopoisk service is unavailable.",
                )
