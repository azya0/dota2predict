from pydantic import BaseModel

from database.models.base import Base
from database.engine import get_async_session


async def get[T: Base](orm: type[T], id: int) -> T:
    async with await get_async_session() as session:
        return await session.get(orm, id)


async def post[T: Base](orm: type[T], schema: BaseModel) -> T:
    async with await get_async_session() as session:
        object = orm(**schema.model_dump())

        session.add(object)

        await session.commit()
        await session.refresh(object)
    
    return object


async def update[T: Base](orm: T) -> T:
    async with await get_async_session() as session:
        session.add(orm)

        await session.commit()
        await session.refresh(orm)
    
    return orm
