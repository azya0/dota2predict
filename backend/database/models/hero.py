from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, IntPrimKey


class Hero(Base):
    __tablename__ = "hero"

    id: Mapped[IntPrimKey]
    name: Mapped[str]
