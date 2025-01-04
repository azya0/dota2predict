from datetime import datetime

from database.queries.schemas import MatchForm, HeroForm


def parse_pro_matches(data: list[dict]) -> list[tuple[int, datetime]]:
    result = []
    
    for match in data:
        result.append((
            match["match_id"], datetime.fromtimestamp(match["start_time"])
        ))
    
    return result


def parse_hero(data: dict) -> HeroForm:
    return HeroForm(
        id=data["id"],
        name=data["localized_name"],
    )


def parse_match(data: list[dict], is_pro_match=False) -> MatchForm:
    return MatchForm(
        id=data["match_id"],
        patch=data["patch"],
        duration=data["duration"],
        game_mode=data["game_mode"],
        isRadiantWon=data["radiant_win"],
        isProMatch=is_pro_match,
        date=datetime.fromtimestamp(data["start_time"]),
    )
