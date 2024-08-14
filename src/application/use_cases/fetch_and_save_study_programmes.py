from src.application.interfaces import Savable, StudyProgrammeSource
from src.application.interfaces import Fetchable
from src.domain.entities.study_programme import StudyProgramme


class FetchAndSaveStudyProgrammesUseCase:
    def __init__(
            self,
            codes_source: Fetchable[str],
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
