import datetime

from pydantic import BaseModel


class ID:
    id: int


class PostMatch(BaseModel, ID):
    patch: int
    duration: int
    game_mode: int

    isRadiantWon: bool
    isProMatch: bool

    date: datetime.datetime
