from uuid import uuid4

from asyncpg import Connection  # type: ignore
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


type url = str


class EngineFactory:
    @staticmethod
    def create(async_url: url) -> AsyncEngine:
        return create_async_engine(
            url=async_url,
            echo=False,
            pool_size=0,
            connect_args={"connection_class": CConnection},
        )


class CConnection(Connection):
    def _get_unique_id(self, prefix: str) -> str:
        return f"__asyncpg_{prefix}_{uuid4()}__"
