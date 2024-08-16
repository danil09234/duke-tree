from typing import Protocol, Any


class Logger(Protocol):
    def debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        ...

    def info(self, message: str, *args: Any, **kwargs: Any) -> None:
        ...

    def success(self, message: str, *args: Any, **kwargs: Any) -> None:
        ...

    def warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        ...

    def error(self, message: str, *args: Any, **kwargs: Any) -> None:
        ...

    def exception(self, message: str, *args: Any, **kwargs: Any) -> None:
        ...

    def critical(self, message: str, *args: Any, **kwargs: Any) -> None:
        ...
