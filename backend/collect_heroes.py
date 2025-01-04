from venv import logger
import asyncio

from opendota.parsers.parsers import parse_hero
from opendota.queries.opendota_requests import get_heroes

from database.queries.db_requests import get, post, update
from database.models.hero import Hero


async def collect_heroes():
    logger.log(0, "Start collecting heroes")

    hero_data = await get_heroes()

    for hero in map(lambda hero_dict: parse_hero(hero_dict), hero_data):
        logger.log(0, f"Checking out {hero.name}...")

        if (orm_hero := await get(Hero, hero.id)) is None:
            logger.warning(f"Saving...")
            await post(Hero, hero)
            continue
        
        is_update = False
        
        for key in (hero_dict := hero.model_dump()):
            if getattr(orm_hero, key) != hero_dict[key]:
                is_update = True
                setattr(orm_hero, hero_dict[key])
        
        if is_update:
            logger.warning(f"Updating...")
            await update(orm_hero)


if __name__ == "__main__":
    logger.log(0, "Initialization new event loop")

    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)

    try:
        asyncio.run(collect_heroes())
    finally:
        loop.close()

    