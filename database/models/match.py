from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base, IntPrimKey, CreateDate


class Match(Base):
    __tablename__ = "match"

    id: Mapped[IntPrimKey]
    
    patch: Mapped[int]
    duration: Mapped[int]
    game_mode: Mapped[int]

    isRadiantWon: Mapped[bool]
