import aiohttp

OPENDOTA_URL = "https://api.opendota.com/api"


async def get(url: str) -> list[dict]:
    full_url = f"{OPENDOTA_URL}/{url}"

    async with aiohttp.ClientSession() as session:
        async with session.get(full_url) as response:
            result = await response.json()

            if (status := response.status) != 200:
                raise Exception(f"[{status}] {result["error"]}")
            
            return result
