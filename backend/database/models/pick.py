from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base, IntPrimKey


class Pick(Base):
    __tablename__ = "pick"

    id: Mapped[IntPrimKey]

    hero_id: Mapped[int] = mapped_column(ForeignKey("hero.id"))
    match_id: Mapped[int] = mapped_column(ForeignKey("match.id"))

    is_pick: Mapped[bool]

    order: Mapped[int]
