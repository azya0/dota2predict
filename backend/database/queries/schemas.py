import datetime

from pydantic import BaseModel


class ID:
    id: int


class MatchForm(BaseModel, ID):
    patch: int
    duration: int
    game_mode: int

    isRadiantWon: bool
    isProMatch: bool

    date: datetime.datetime
