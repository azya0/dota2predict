from database.models import Match
from database.engine import get_async_session


async def post_match():
    async with get_async_session() as session:
        