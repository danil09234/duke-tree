import asyncio
from typing import Optional

from src.infrastructure.exceptions import PageLoadingError, InvalidUrlError
from src.infrastructure.interfaces import Repository, WebPageLoader
from src.domain.entities.languages import Language


class TukeStudyProgrammePageFetcher(Repository[str]):
    _PROGRAMME_PAGE_URL_TEMPLATE = "https://res.tuke.sk/api/programme_detail/{code}?lang={lang}"

    def __init__(self, study_programmes_codes_fetcher: Repository[str], page_loader: WebPageLoader):
        self._study_programmes_codes_fetcher = study_programmes_codes_fetcher
        self._page_loader = page_loader

    @classmethod
    def _get_page_url(cls, study_programme_code: str, language: Language) -> str:
        return cls._PROGRAMME_PAGE_URL_TEMPLATE.format(code=study_programme_code, lang=language.value)

    async def _fetch_with_error_handling(self, url: str) -> Optional[str]:
        try:
            return await self._page_loader.load(url)
        except PageLoadingError:
            return None
        except InvalidUrlError as e:
            raise InvalidUrlError from e

    async def fetch_all(self) -> list[str]:
        study_programmes_codes = await self._study_programmes_codes_fetcher.fetch_all()

        tasks = []

        for study_programme_code in study_programmes_codes:
            for language in Language:
                page_url = self._get_page_url(study_programme_code, language)
                tasks.append(self._fetch_with_error_handling(page_url))

        study_programmes_pages = list(await asyncio.gather(*tasks))
        study_programmes_pages = filter(lambda page: page is not None, study_programmes_pages)

        return study_programmes_pages
