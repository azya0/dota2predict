from opendota.queries.base import get, aiohttp


async def get_pro_matches() -> aiohttp.ClientResponse:
    return await get("proMatches")


async def get_match(id: int) -> aiohttp.ClientResponse:
    return await get(f"matches/{id}")
