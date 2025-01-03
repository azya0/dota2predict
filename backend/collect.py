from opendota.parsers.parsers import parse_match
from opendota.queries.database_requests import save_match

import asyncio

if __name__ == "__main__":
    asyncio.run(save_match(parse_match(8110368938)))
