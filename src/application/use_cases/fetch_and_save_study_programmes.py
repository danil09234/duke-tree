from src.application.interfaces import Savable, StudyProgrammesSource
from src.application.interfaces import Fetchable


class FetchAndSaveStudyProgrammesUseCase[StudyProgrammeData]:
    def __init__(
            self,
            codes_source: Fetchable[str],
            study_programmes_source: StudyProgrammesSource[StudyProgrammeData],
            storage: Savable[StudyProgrammeData]
    ):
        self._codes_source = codes_source
        self._study_programmes_source = study_programmes_source
        self._storage = storage

    async def __call__(self) -> None:
        """
        Fetches and saves the list of study programmes.
        """
        study_programme_codes = await self._codes_source.fetch_all()
        study_programmes = await self._study_programmes_source.get_by_codes(study_programme_codes)
        await self._storage.save_multiple(study_programmes)
