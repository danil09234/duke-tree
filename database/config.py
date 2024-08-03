from .exceptions.config import SyncDatabaseUrlNotInitialized, AsyncDatabaseUrlNotInitialized, InvalidDatabaseUrlType

__SYNC_DATABASE_URL = ""
__ASYNC_DATABASE_URL = ""


def get_sync_database_url() -> str:
    global __SYNC_DATABASE_URL
    if not __SYNC_DATABASE_URL:
        raise SyncDatabaseUrlNotInitialized
    return __SYNC_DATABASE_URL


def get_async_database_url() -> str:
    global __ASYNC_DATABASE_URL
    if not __SYNC_DATABASE_URL:
        raise AsyncDatabaseUrlNotInitialized
    return __ASYNC_DATABASE_URL


def set_sync_database_url(url: str) -> None:
    if not isinstance(url, str):
        raise InvalidDatabaseUrlType
    global __SYNC_DATABASE_URL
    __SYNC_DATABASE_URL = url


def set_async_database_url(url: str) -> None:
    if not isinstance(url, str):
        raise InvalidDatabaseUrlType
    global __ASYNC_DATABASE_URL
    __ASYNC_DATABASE_URL = url
