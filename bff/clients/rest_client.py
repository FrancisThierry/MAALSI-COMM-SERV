import httpx
from core.config import settings

async def fetch_from_rest(endpoint: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.REST_BACKEND_URL}{endpoint}")
        response.raise_for_status()
        return response.json()