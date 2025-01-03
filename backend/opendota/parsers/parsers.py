from datetime import datetime

from opendota.queries.opendota_requests import get_match
from database.queries.schemas import MatchForm


def parse_pro_matches(data: list[dict]) -> list[tuple[int, datetime]]:
    result = []
    
    for match in data:
        result.append((
            match["match_id"], datetime.fromtimestamp(match["start_time"])
        ))
    
    return result


def parse_match(id: int, isProMatch: bool = False) -> MatchForm:
    data: dict = get_match(id).json()

    return MatchForm(
        id=data["match_id"],
        patch=data["patch"],
        duration=data["duration"],
        game_mode=data["game_mode"],
        isRadiantWon=data["radiant_win"],
        isProMatch=isProMatch,
        date=datetime.fromtimestamp(data["start_time"])
    )
