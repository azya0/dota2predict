from venv import logger
from typing import Coroutine

from logger import getLogger, logging
from opendota.parsers.parsers import parse_match, parse_pro_matches
from opendota.queries.opendota_requests import get_pro_matches, get_match
from opendota.queries.database_requests import get_match as get_match_from_db, save_match

import asyncio


async def wait_for_limit(corutine: Coroutine, time: int):
    await asyncio.sleep(time)

    return await corutine


async def collect_pro_matches(logger: logging.Logger):
    logger.info("Start collecting pro matches")

    matches_id = []

    pro_matches = await get_pro_matches()

    for counting, (id, _) in enumerate(parse_pro_matches(pro_matches)):
        if (await get_match_from_db(id)) is not None:
            continue
        
        logger.info(f"Collecting pro match with id {counting}")

        matches_id.append(id)
    
    if not matches_id:
        logger.info("No new pro matches")
        return

    matches_data: list[list[dict] | Exception] = await asyncio.gather(
        *map(lambda id: get_match(id), matches_id), return_exceptions=True
    )

    final_corutines = []
    is_day_limit = False

    while matches_id:
        new_matches_id = []

        for index, match_data in enumerate(matches_data):
            if not isinstance(match_data, Exception):
                parsed_match = parse_match(match_data, is_pro_match=True)
                final_corutines.append(save_match(parsed_match))

                continue
            
            reason = " ".join(str(match_data).split()[1:])

            match reason:
                case "minute rate limit exceeded":
                    new_matches_id.append(matches_id[index])
                    break
                case "day limit exceeded":
                    is_day_limit = True
                    break
                case _:
                    raise Exception(reason)
        
        if is_day_limit:
            logger.warning(f"Day limit. Saving {len(final_corutines)} matches...")
            break

        matches_id = new_matches_id

        logger.warning(f"Limited: {len(matches_id)}")

        matches_data = await asyncio.gather(*map(lambda id: wait_for_limit(get_match(id), 60), matches_id), return_exceptions=True)
    
    logger.info("Saving data")

    await asyncio.gather(*final_corutines, return_exceptions=True)

    logger.info("Saving complete")


if __name__ == "__main__":
    logger = getLogger("collect pro matches")
    
    logger.info("Initialization new event loop")

    try:
        loop = asyncio.new_event_loop()

        asyncio.set_event_loop(loop)

        asyncio.run(collect_pro_matches(logger))
    finally:
        loop.close()
