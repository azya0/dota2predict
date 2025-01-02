from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base, IntPrimKey


class Match(Base):
    __tablename__ = "match"

    id: Mapped[IntPrimKey]
    
    patch: Mapped[int]
    duration: Mapped[int]
    game_mode: Mapped[int]

    isRadiantWon: Mapped[bool]
    isProMatch: Mapped[bool]

    date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
