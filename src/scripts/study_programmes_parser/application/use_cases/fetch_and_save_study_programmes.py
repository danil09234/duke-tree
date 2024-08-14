from src.scripts.study_programmes_parser.infrastructure.interfaces import Savable, Parser, \
    StudyProgrammeSource
from src.scripts.study_programmes_parser.infrastructure.interfaces import Repository
from src.scripts.study_programmes_parser.domain.entities.study_programme import StudyProgramme


class FetchAndSaveStudyProgrammesUseCase:
    def __init__(self, source: Repository[StudyProgramme], storage: Savable[StudyProgramme]):
        self._source = source
        self._storage = storage

    async def execute(self) -> None:
        """
        Fetches and saves the list of study programmes.
        """
        study_programmes = await self._source.fetch_all()
        await self._storage.save_multiple(study_programmes)


class FetchAndSaveStudyProgrammesUseCase2:
    def __init__(
            self,
            all_pages_fetcher: Repository,
            parser: Parser[StudyProgramme],
            storage: Savable[StudyProgramme]
    ):
        self._all_pages_fetcher = all_pages_fetcher
        self._parser = parser
        self._storage = storage

    async def execute(self) -> None:
        """
        Fetches and saves the list of study programmes.
        """
        study_programmes_pages = await self._all_pages_fetcher.fetch_all()
        study_programmes = [self._parser.parse(page) for page in study_programmes_pages]
        await self._storage.save_multiple(study_programmes)


class FetchAndSaveStudyProgrammesUseCase3:
    def __init__(
            self,
            codes_source: Repository[str],
            study_programme_source: StudyProgrammeSource,
            storage: Savable[StudyProgramme]
    ):
        self._codes_source = codes_source
        self._study_programmes_source = study_programme_source
        self._storage = storage

    async def __call__(self) -> None:
        """
        Fetches and saves the list of study programmes.
        """
        study_programme_codes = await self._codes_source.fetch_all()
        study_programmes = await self._study_programmes_source.get_by_codes(study_programme_codes)
        await self._storage.save_multiple(study_programmes)
