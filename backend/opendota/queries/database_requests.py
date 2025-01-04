from database.queries.db_requests import post, get
from database.queries.schemas import MatchForm
from database.models.match import Match


async def save_match(data: MatchForm):
    await post(Match, data)


async def get_match(id: int):
    return await get(Match, id)
