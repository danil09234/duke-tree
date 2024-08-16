from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession

from src.application.interfaces import Creator


class SessionMakerFactory(Creator[async_sessionmaker[AsyncSession]]):
    def __init__(self, engine: AsyncEngine) -> None:
        self._engine = engine

    def create(self) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(bind=self._engine, autoflush=False, expire_on_commit=False)
