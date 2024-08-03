class DatabaseUrlNotInitialized(Exception):
    pass


class SyncDatabaseUrlNotInitialized(DatabaseUrlNotInitialized):
    pass


class AsyncDatabaseUrlNotInitialized(DatabaseUrlNotInitialized):
    pass


class InvalidDatabaseUrl(Exception):
    pass


class InvalidDatabaseUrlType(Exception):
    pass
