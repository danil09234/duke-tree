from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession


class SessionMakerFactory:
    @staticmethod
    def create(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
