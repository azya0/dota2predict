from venv import logger
from typing import Coroutine

from opendota.parsers.parsers import parse_match, parse_pro_matches
from opendota.queries.opendota_requests import get_pro_matches, get_match
from opendota.queries.database_requests import get_match as get_match_from_db, save_match

import asyncio


async def wait_for_limit(corutine: Coroutine, time: int):
    await asyncio.sleep(time)

    return await corutine


async def collect_pro_matches():
    logger.log(0, "Starting script...")

    matches_id = []

    for counting, (id, _) in enumerate(parse_pro_matches(await get_pro_matches())):
        if (await get_match_from_db(id)) is not None:
            continue
        
        logger.log(0, f"Collecting pro matches id {counting}...")

        matches_id.append(id)

    matches_data: list[list[dict] | Exception] = await asyncio.gather(
        *map(lambda id: get_match(id), matches_id), return_exceptions=True
    )

    final_corutines = []

    while matches_id:
        new_matches_id = []

        for index, match_data in enumerate(matches_data):
            if not isinstance(match_data, Exception):
                final_corutines.append(
                    save_match(parse_match(match_data, is_pro_match=True))
                )

                continue
            
            if (reason := " ".join(str(match_data).split()[1:])) != "minute rate limit exceeded":
                raise Exception(reason)
            
            new_matches_id.append(matches_id[index])
        
        matches_id = new_matches_id

        logger.warning(f"Limited: {len(matches_id)}")

        matches_data = await asyncio.gather(*map(lambda id: wait_for_limit(get_match(id), 60), matches_id), return_exceptions=True)
    
    logger.log(0, "Saving data")

    await asyncio.gather(*final_corutines, return_exceptions=True)

    logger.log(0, "Saving complete")


if __name__ == "__main__":
    logger.log(0, "Initialization new event loop")

    try:
        loop = asyncio.new_event_loop()

        asyncio.set_event_loop(loop)

        asyncio.run(collect_pro_matches())
    finally:
        loop.close()
