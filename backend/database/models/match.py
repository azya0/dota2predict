from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import BigInteger

from .base import Base


class Match(Base):
    __tablename__ = "match"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    
    patch: Mapped[int]
    duration: Mapped[int]
    game_mode: Mapped[int]

    isRadiantWon: Mapped[bool]
    isProMatch: Mapped[bool]

    date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
