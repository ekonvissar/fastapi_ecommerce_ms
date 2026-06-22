import httpx

from app.config import Settings


class IdentityClient:
    def __init__(self, http: httpx.AsyncClient, settings: Settings) -> None:
        self._http = http
        self._base = settings.identity_url.rstrip("/")

    async def register(self, payload: dict) -> httpx.Response:
        return await self._http.post(f"{self._base}/users/", json=payload)

    async def login(self, username: str, password: str) -> httpx.Response:
        return await self._http.post(
            f"{self._base}/users/token",
            data={"username": username, "password": password},
        )

    async def refresh(self, refresh_token: str | None) -> httpx.Response:
        cookies = {}
        if refresh_token:
            cookies["refresh_token"] = refresh_token
        return await self._http.post(f"{self._base}/users/refresh", cookies=cookies)

    async def logout(self, refresh_token: str | None) -> httpx.Response:
        cookies = {}
        if refresh_token:
            cookies["refresh_token"] = refresh_token
        return await self._http.post(f"{self._base}/users/logout", cookies=cookies)
