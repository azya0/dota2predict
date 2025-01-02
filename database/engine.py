from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from typing_extensions import AsyncGenerator

from config import get_settings

class SessionManager:
    def __init__(self):
        settings = get_settings()
        self.async_engine = create_async_engine(
            url=settings.SQLALCHEMY_URL,
            echo=False,
            pool_size=5,
            max_overflow=10
        )
        
        self.async_session = sessionmaker(
            self.async_engine,
            expire_on_commit=False,
            class_=AsyncSession
        )

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    def get_session(self) -> Session | AsyncSession:
        return self.async_session()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = SessionManager().get_session()

    async with async_session:
        try:
            yield async_session
            await async_session.commit()
        except SQLAlchemyError as exc:
            await async_session.rollback()
            raise exc
        finally:
            await async_session.close()
