from uuid import uuid4

from asyncpg import Connection  # type: ignore
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from src.application.interfaces import Creator

type url = str


class EngineFactory(Creator[AsyncEngine]):
    def __init__(self, async_url: url) -> None:
        self._async_url = async_url

    def create(self) -> AsyncEngine:
        return create_async_engine(
            url=self._async_url,
            echo=False,
            pool_size=0,
            connect_args={"connection_class": CConnection},
        )


class CConnection(Connection):
    def _get_unique_id(self, prefix: str) -> str:
        return f"__asyncpg_{prefix}_{uuid4()}__"
