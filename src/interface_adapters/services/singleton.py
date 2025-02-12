from threading import Lock
from typing import Any


class Singleton(type):
    _instances: dict[type, type] = {}
    _lock = Lock()

    def __call__(cls, *args: list[Any], **kwargs: list[Any]) -> type:
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
