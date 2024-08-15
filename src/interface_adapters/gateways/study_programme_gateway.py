import asyncio
from typing import Optional, Generator, Coroutine, Any

from src.domain.entities import StudyProgramme
from src.domain.enums import Language
from src.interface_adapters.exceptions import PageLoadingError, InvalidUrlError
from src.application.interfaces import StudyProgrammeSource, WebPageLoader, Parser


class StudyProgrammeGateway(StudyProgrammeSource):
    _PROGRAMME_PAGE_URL_TEMPLATE = "https://res.tuke.sk/api/programme_detail/{code}?lang={lang}"

    def __init__(self, loader: WebPageLoader, parser: Parser[str, StudyProgramme]):
        self._loader = loader
        self._parser = parser

    @classmethod
    def _get_page_url(cls, study_programme_code: str, language: Language) -> str:
        return cls._PROGRAMME_PAGE_URL_TEMPLATE.format(code=study_programme_code, lang=language.value)

    async def _load_with_error_handling(self, url: str) -> Optional[str]:
        try:
            return await self._loader.load(url)
        except PageLoadingError:
            return None
        except InvalidUrlError as e:
            raise InvalidUrlError from e

    async def get_by_codes(self, programmes_codes: list[str]) -> list[StudyProgramme]:
        pages = await asyncio.gather(*await self._get_all_pages_loading_coroutines(programmes_codes))
        without_none_pages = [page for page in pages if page is not None]
        return self._parser.parse_multiple(without_none_pages)

    async def _get_all_pages_loading_coroutines(self, programmes_codes: list[str]) \
            -> Generator[Coroutine[Any, Any, Optional[str]], None, None]:
        return (
            self._load_with_error_handling(self._get_page_url(code, language))
            for code in programmes_codes for language in Language
        )
