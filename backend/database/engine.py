from functools import lru_cache
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session
from typing_extensions import AsyncGenerator

from database.config import get_settings

class SessionManager:
    def __init__(self):
        self.async_engine = create_async_engine(
            url=get_settings().SQLALCHEMY_URL,
            echo=False,
            pool_size=5,
            max_overflow=10
        )
        
        self.async_session = async_sessionmaker(
            self.async_engine
        )

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    def get_session(self) -> Session | AsyncSession:
        return self.async_session()


@lru_cache
def get_session_manager() -> SessionManager:
    return SessionManager()


async def get_async_session() -> AsyncSession:
    return get_session_manager().get_session()


async def get_async_session_generator() -> AsyncGenerator[AsyncSession, None]:
    async_session = get_session_manager().get_session()

    async with async_session:
        try:
            yield async_session
            await async_session.commit()
        except SQLAlchemyError as exc:
            await async_session.rollback()
            raise exc
