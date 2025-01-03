from pydantic import BaseModel

from database.models.base import Base
from database.engine import get_async_session


async def post(orm: type[Base], schema: type[BaseModel]):
    async with await get_async_session() as session:
        session.add(orm(**schema.model_dump()))

        await session.commit()
