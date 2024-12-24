from src.application.interfaces import GetAllRepository, Fetchable, StudyProgrammesRepositoryByCodes
from src.domain.entities.res_tuke_study_programme_data import ResTukeStudyProgrammeData


class AllResTukeStudyProgrammesRepository(GetAllRepository[ResTukeStudyProgrammeData]):
    def __init__(
            self,
            study_programmes_codes_source: Fetchable[str],
            study_programmes_repository: StudyProgrammesRepositoryByCodes[ResTukeStudyProgrammeData]
    ) -> None:
        self._study_programmes_codes_source = study_programmes_codes_source
        self._study_programmes_repository = study_programmes_repository

    async def get_all(self) -> list[ResTukeStudyProgrammeData]:
        study_programmes_codes = await self._study_programmes_codes_source.fetch_all()
        study_programmes = await self._study_programmes_repository.get_by_codes(study_programmes_codes)
        return study_programmes
