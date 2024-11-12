import asyncio
from abc import ABC
from typing import Generator, Coroutine, Any, Optional, Iterable

from src.interface_adapters.exceptions import InvalidUrlError, PageLoadingError
from src.domain.enums import Language
from src.application.interfaces import WebPageLoader, Parser


class StudyProgrammesGatewayBase[O](ABC):
    _URL_TEMPLATE = "https://www.example.com/{lang}/{code}"

    def __init__(self, loader: WebPageLoader, parser: Parser[str, O]):
        self._loader = loader
        self._parser = parser

    async def get_by_codes(self, programmes_codes: list[str]) -> list[O]:
        all_page_loading_coroutines = self._get_all_pages_loading_coroutines_generator(programmes_codes)
        gathered_values = await asyncio.gather(*all_page_loading_coroutines)
        pages = self._remove_none_values(gathered_values)
        return self._parser.parse_multiple(pages)

    def _get_all_pages_loading_coroutines_generator(self, programmes_codes: list[str]) \
            -> Generator[Coroutine[Any, Any, Optional[str]], None, None]:
        return (
            self._load_with_error_handling(self._get_page_url(code, language))
            for code in programmes_codes for language in Language
        )

    @classmethod
    def _get_page_url(cls, study_programme_code: str, language: Language) -> str:
        return cls._URL_TEMPLATE.format(code=study_programme_code, lang=language.value)

    async def _load_with_error_handling(self, url: str) -> Optional[str]:
        try:
            return await self._loader.load(url)
        except PageLoadingError:
            return None
        except InvalidUrlError as e:
            raise InvalidUrlError from e

    @staticmethod
    def _remove_none_values[T](source: Iterable[T | None]) -> list[T]:
        return [value for value in source if value is not None]
