from opendota.queries.base import get, aiohttp


async def get_pro_matches() -> list[dict]:
    return await get("proMatches")


async def get_match(id: int) -> dict:
    return await get(f"matches/{id}")


async def get_heroes() -> list[dict]:
    return await get(f"/heroes")