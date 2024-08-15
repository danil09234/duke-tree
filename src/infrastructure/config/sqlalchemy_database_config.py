from os import getenv
from typing import Type

from sqlalchemy.orm import DeclarativeBase

from src.infrastructure.interfaces import DatabaseConfig
from src.infrastructure.orm.exceptions import DatabaseUserNotSetError, DatabasePasswordNotSetError, \
    DatabaseHostNotSetError, DatabasePortNotSetError, DatabaseNameNotSetError


class SQLAlchemyDatabaseConfig(DatabaseConfig):
    def _build_sync_database_url(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    def _build_async_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    def __init__(self) -> None:
        self._init_db_user()
        self._init_db_password()
        self._init_db_host()
        self._init_db_port()
        self._init_db_name()

        self._sync_database_url = self._build_sync_database_url()
        self._async_database_url = self._build_async_database_url()
        self._defaults: list[Type[DeclarativeBase]] = []

    def _init_db_name(self):
        self._db_name = getenv("db_name")
        if not self._db_name:
            raise DatabaseNameNotSetError

    def _init_db_port(self):
        self._db_port = getenv("db_port")
        if not self._db_port:
            raise DatabasePortNotSetError

    def _init_db_host(self):
        self._db_host = getenv("db_host")
        if not self._db_host:
            raise DatabaseHostNotSetError

    def _init_db_password(self):
        self._db_password = getenv("db_password")
        if not self._db_password:
            raise DatabasePasswordNotSetError

    def _init_db_user(self):
        self._db_user = getenv("db_user")
        if not self._db_user:
            raise DatabaseUserNotSetError

    @property
    def db_user(self) -> str:
        return self._db_user

    @property
    def db_password(self) -> str:
        return self._db_password

    @property
    def db_host(self) -> str:
        return self._db_host

    @property
    def db_port(self) -> str:
        return self._db_port

    @property
    def db_name(self) -> str:
        return self._db_name

    @property
    def defaults(self) -> list[Type[DeclarativeBase]]:
        return self._defaults

    @defaults.setter
    def defaults(self, defaults: list[Type[DeclarativeBase]]) -> None:
        self._defaults = defaults

    @property
    def sync_database_url(self) -> str:
        return self._sync_database_url

    @property
    def async_database_url(self) -> str:
        return self._async_database_url
