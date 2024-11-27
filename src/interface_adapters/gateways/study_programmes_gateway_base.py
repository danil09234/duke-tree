import asyncio
from abc import ABC
from typing import Generator, Coroutine, Any, Optional, Iterable, NamedTuple

from src.interface_adapters.exceptions import InvalidUrlError, PageLoadingError
from src.domain.enums import Language
from src.application.interfaces import WebPageLoader, Parser, LanguageParserFactory


class PageMetadata(NamedTuple):
    language: Language
    code: str
    url: str


class Page[Data](NamedTuple):
    data: Data
    metadata: PageMetadata


class StudyProgrammesGatewayBase[Data](ABC):
    _URL_TEMPLATE = "https://www.example.com/{lang}/{code}"

    def __init__(self, loader: WebPageLoader, language_parser_factory: LanguageParserFactory[Parser[str, Data]]):
        self._loader = loader
        self._language_parser_factory = language_parser_factory

    async def get_by_codes(self, programmes_codes: list[str]) -> list[Page[Data]]:
        all_page_loading_coroutines = self._get_all_pages_loading_coroutines_generator(programmes_codes)
        gathered_values = await asyncio.gather(*all_page_loading_coroutines)
        pages = self._remove_none_values(gathered_values)
        return self._apply_parser(pages)

    def _get_all_pages_loading_coroutines_generator(self, programmes_codes: list[str]) \
            -> Generator[Coroutine[Any, Any, Optional[Page[str]]], None, None]:
        for language in Language:
            for code in programmes_codes:
                page_url = self._get_page_url(code, language)
                yield self._load_with_metadata(PageMetadata(language, code, page_url))

    @classmethod
    def _get_page_url(cls, study_programme_code: str, language: Language) -> str:
        return cls._URL_TEMPLATE.format(code=study_programme_code, lang=language.value)

    async def _load_with_metadata(self, metadata: PageMetadata) -> Optional[Page[str]]:
        page_text = await self._load_with_error_handling(metadata.url)
        if not page_text:
            return None
        return Page(data=page_text, metadata=metadata)

    async def _load_with_error_handling(self, url: str) -> Optional[str]:
        try:
            return await self._loader.load(url)
        except PageLoadingError:
            return None
        except InvalidUrlError as e:
            raise InvalidUrlError from e

    @staticmethod
    def _remove_none_values[Item](source: Iterable[Optional[Item]]) -> list[Item]:
        return [value for value in source if value is not None]

    def _apply_parser(self, pages: list[Page[str]]) -> list[Page[Data]]:
        return list(
            map(
                lambda page: Page(
                    data=self._language_parser_factory.create(page.metadata.language).parse_one(page.data),
                    metadata=page.metadata
                ),
                pages
            )
        )
