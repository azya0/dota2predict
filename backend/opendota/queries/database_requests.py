from database.queries.db_requests import post
from database.queries.schemas import MatchForm
from database.models.match import Match


async def save_match(data: MatchForm):
    await post(Match, data)
