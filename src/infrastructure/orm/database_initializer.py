from typing import Type

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy_utils import database_exists, create_database  # type: ignore

from src.infrastructure.interfaces import DatabaseConfig
from loguru import logger


class DatabaseInitializer:
    def __init__(
            self,
            engine: AsyncEngine,
            session_maker: async_sessionmaker[AsyncSession],
            base: Type[DeclarativeBase],
            config: DatabaseConfig[Type[DeclarativeBase]]
    ):
        self._engine = engine
        self._session_maker = session_maker
        self._base = base
        self._config = config

    async def init_models(self) -> None:
        logger.info("Initializing models")
        async with self._engine.begin() as connection:
            logger.warning("Dropping all tables")
            await connection.run_sync(self._base.metadata.drop_all)
            logger.info("Creating all tables")
            await connection.run_sync(self._base.metadata.create_all)
            await connection.commit()

    async def add_defaults(self) -> None:
        logger.info("Adding defaults")
        async with self._session_maker() as session:
            session.add_all(self._config.defaults)
            await session.commit()
            logger.success("Defaults were added")

    async def init_database(self, fresh_init: bool = False) -> None:
        sync_url = self._config.sync_database_url
        if fresh_init:
            if not database_exists(sync_url):
                logger.info("Creating database")
                create_database(sync_url)
                logger.success("Database was created")
            else:
                logger.info("Database was found")
            await self.init_models()
            await self.add_defaults()
        else:
            if not database_exists(sync_url):
                logger.info("Creating database")
                create_database(sync_url)
                logger.success("Database was created")
            else:
                logger.info("Database was found")

        logger.success("Database initialization was finished")
