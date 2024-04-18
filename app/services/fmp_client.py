from httpx import AsyncClient

from app.config import FMP_API_KEY, FMP_API_URL

API_V3 = "v3"
API_V4 = "v4"


async def get_full_quotes_list(client: AsyncClient) -> list:
    endpoint = f"quotes/crypto"
    data = await _fetch(client, endpoint)
    if not data:
        raise ValueError
    return list(data)


async def _fetch(
    client: AsyncClient, endpoint: str, api_version: str = API_V3, params: dict = None
):
    if params is None:
        params = {"apikey": FMP_API_KEY}
    else:
        params.update({"apikey": FMP_API_KEY})

    url = f"{FMP_API_URL}/{api_version}/{endpoint}"
    r = await client.get(url, params=params, timeout=10)
    r.raise_for_status()
    return r.json()
