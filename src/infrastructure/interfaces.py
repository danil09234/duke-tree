from typing import Protocol


class DatabaseConfig[T](Protocol):
    @property
    def sync_database_url(self) -> str:
        ...

    @property
    def async_database_url(self) -> str:
        ...

    @property
    def defaults(self) -> list[T]:
        ...


class EntityMapper[E, M](Protocol):
    async def to_entity(self, source: M) -> E:
        ...

    async def from_entity(self, entity: E) -> M:
        ...
