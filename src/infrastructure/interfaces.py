from typing import Protocol


class DatabaseConfig(Protocol):
    @property
    def sync_database_url(self) -> str:
        ...

    @property
    def async_database_url(self) -> str:
        ...

    @property
    def defaults(self) -> list:
        ...


class EntityMapper[E, M](Protocol):
    async def to_entity(self, source: M) -> E:
        ...

    async def from_entity(self, entity: E) -> M:
        ...
